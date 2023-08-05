# (c) Copyright 2022 Aaron Kimball
#
# Methods for capturing and reloading state from running Arduino.

import os.path
import threading
import time

import arduino_dbg.debugger as debugger
import arduino_dbg.io as io
import arduino_dbg.protocol as protocol
import arduino_dbg.serialize as serialize

SERIALIZED_STATE_KEY = 'state'

DUMP_SCHEMA_KEY = 'dump_schema'
DUMP_SCHEMA_VER = 1


def capture_dump(debugger, dump_filename):
    """
    Capture registers and SRAM from the device and store in a file locally.

    Assumes that the remote instance is already paused and ready for commands
    from the debugger.
    """

    elf_file_name = debugger.elf_name

    # Get this upfront; force architecture resolution before reading arch conf.
    arch_specs = debugger.get_arch_specs()

    ram_start = debugger.get_arch_conf("RAMSTART")
    ram_end = debugger.get_arch_conf("RAMEND")
    instruction_set = debugger.get_arch_conf("instruction_set")
    gen_reg_count = debugger.get_arch_conf("general_regs")
    byte_order = debugger.get_arch_conf("endian")  # 'little' or 'big'

    platform_name = debugger.get_conf('arduino.platform')
    arch_name = debugger.get_conf('arduino.arch')

    # Number of bytes to retrieve from the device at a time
    read_size = 4  # TODO(aaron): Parameterize?

    # what's the memory address where this starts?
    if instruction_set == 'avr':
        # On AVR, we skip the first few bytes from 0 because those are mem-mapped to registers.
        # We'll populate those directly from the register dump.
        # We do read the extended memory-mapped register set from RAM, here, even though it is
        # below RAMSTART.
        #
        # Since we also include $SP and $SREG in registers, we need to sync those
        # mem-mapped positions to the register file values before we write this dump.
        sram_offset = gen_reg_count
    else:
        sram_offset = ram_start


    # list of `bytes` objects to hold memory dump
    sram_bytes = []
    # Retrieve the RAM from the device.
    for read_at in range(sram_offset, ram_end, read_size):
        v = debugger.get_sram(read_at, read_size)
        ram_word = v.to_bytes(read_size, byteorder=byte_order)
        sram_bytes.append(ram_word)
    sram_byte_string = bytearray(b''.join(sram_bytes))

    regs = debugger.get_registers()

    memstats = debugger.get_memstats()
    del memstats['RAMSTART']  # Remove memstats components that are populated from _arch.
    del memstats['RAMEND']
    del memstats['FLASHEND']

    num_gpio = debugger.get_platform_conf("gpio_pins")
    gpio = []
    for i in range(0, num_gpio):
        gpio.append(debugger.get_gpio_value(i))

    if instruction_set == 'avr':
        # Prepend general-purpose register file data to the beginning of the RAM image.
        reg_bytes = bytearray()
        for i in range(0, gen_reg_count):
            reg_bytes.append(regs[f'r{i}'])
        sram_byte_string[0:0] = reg_bytes
        sram_offset = 0  # We now have a complete memory image starting at offset 0000h

        # Make sure register-file values for $SP and $SREG are written to the SRAM image
        # at the right mem-mapped-register addresses, so they are consistent on reload.
        spl_port = debugger.get_arch_conf("SPL_PORT")
        has_sph = debugger.get_arch_conf("has_sph")
        if has_sph:
            sph_port = debugger.get_arch_conf("SPH_PORT")
        sreg_port = debugger.get_arch_conf("SREG_PORT")

        avr_port_offset = debugger.get_arch_conf("AVR_PORT_OFFSET")

        sram_byte_string[avr_port_offset + spl_port] = regs["SP"] & 0xFF
        if has_sph:
            sram_byte_string[avr_port_offset + sph_port] = (regs["SP"] >> 8) & 0xFF

        sram_byte_string[avr_port_offset + sreg_port] = regs["SREG"] & 0xFF

    # Gather together the components we need to serialize.
    out = {}
    out['platform'] = platform_name
    out['arch'] = arch_name
    out['elf_file_name'] = elf_file_name
    out['ram_image'] = bytes(sram_byte_string)
    out['ram_image_start'] = sram_offset
    out['registers'] = regs
    out['memstats'] = memstats
    out['gpio'] = gpio
    out['arch_specs'] = arch_specs
    out[DUMP_SCHEMA_KEY] = DUMP_SCHEMA_VER

    serialize.persist_config_file(dump_filename, SERIALIZED_STATE_KEY, out)


def load_dump(filename, print_q, config=None, history_change_hook=None):
    """
    Load a dump file and initialize a debugger instance around it.

    @param filename the dump file to load.
    @param print_q the queue to connect the new Debugger to stdout/ConsolePrinter.
    @param config optional debugger config to override defaults & saved cfg file settings.
        If non-None, also prevents Debugger from persisting config changes via `set` kwd.
    @param history_change_hook a callback fn to install in the new Debugger for history filename.

    @return a pair containing (new_debugger, hosted_debug_service).
    """

    # Load the data out of the file...
    dump_data = serialize.load_config_file(print_q, filename, SERIALIZED_STATE_KEY)

    # Make a pair of pipes that can communicate with one another.
    (left, right) = io.make_bidi_pipe()

    # Make the ELF filename absolute. If the filename in the dump is relative,
    # it is relative to the location of the dump file, not the cwd.
    if os.path.isabs(filename):
        canonical_dump_filename = os.path.normpath(filename)
    else:
        canonical_dump_filename = os.path.abspath(filename)
    dump_dir = os.path.dirname(canonical_dump_filename)

    elf_filename = dump_data['elf_file_name']
    if not os.path.isabs(elf_filename):
        # ELF filename is relative.
        elf_filename = os.path.join(dump_dir, elf_filename)
        elf_filename = os.path.normpath(elf_filename)

    # Create a new Debugger instance connected to the 'left' pipe.
    # Specify the ELF file associated with this dump and the relevant Arduino platform.
    # Start with client lock ownership - we'll release it when this 'load' command is done.
    dbg = debugger.Debugger(
        elf_filename, left, print_q,
        arduino_platform=dump_data['platform'], force_config=config,
        history_change_hook=history_change_hook, is_locked=True)
    dbg.set_process_state(debugger.ProcessState.BREAK)  # It's definitionally always paused.

    # The debugger will not send a 'break' out of the gate, so the protocol version handshake
    # won't happen. Pre-initialize the protocol version from the handshake to the ver we speak.
    dbg._protocol_version = debugger.HOST_MAX_PROTOCOL_VERSION

    # Create a service that acts like the __dbg_service() in C.
    # Connect it to the ram/image and the 'right' pipe.
    dbg_serv = HostedDebugService(dump_data, dbg, right)
    dbg_serv.start()  # Start service in a new thread.

    return (dbg, dbg_serv)


class HostedDebugService(object):
    """
    A service that can emulate the __dbg_service() library method locally, from a snapshot of RAM
    and registers.
    """
    def __init__(self, dump_data, debugger, conn):
        self._conn = conn
        self._debugger = debugger

        if dump_data[DUMP_SCHEMA_KEY] > DUMP_SCHEMA_VER:
            raise Exception(f"Cannot load dump schema with version={dump_data[DUMP_SCHEMA_KEY]}")

        self._memory = bytearray(dump_data['ram_image'])
        # Do memory addrs start from 0h? Or is the .data/.bss/SRAM segment loaded at an offset?
        self._memory_segment_offset = dump_data['ram_image_start'] or 0
        self._regs = dump_data['registers']

        self._memstats = None
        if 'memstats' in dump_data:
            self._memstats = dump_data['memstats']
        else:
            self._memstats = {}

        self._num_gpio = self._debugger.get_platform_conf("gpio_pins")
        self._gpio = self._num_gpio * [0]
        if 'gpio' in dump_data:
            self._gpio = dump_data['gpio']
        else:
            self._gpio = []

        if 'arch_specs' in dump_data:
            self._arch_specs = dump_data['arch_specs']
        else:
            self._arch_specs = []

        self.platform = dump_data['platform']
        self.arch = dump_data['arch']
        self.elf_file_name = dump_data['elf_file_name']

        self.stay_alive = True
        self.thread = threading.Thread(target=self.service, name="Hosted debug service")

    def start(self):
        # start this in a new thread.
        self.thread.start()

    def shutdown(self, wait=True):
        """
        Stop the service.
        """
        self.stay_alive = False
        if wait:
            self.thread.join()


    def _get_ram(self, mem_slice):
        """
        Return the bytes in RAM as specified by the slice 'mem_slice'.
        mem_slice should be specified as an on-CPU address.
        """
        start = None
        end = None
        if mem_slice.start is not None:
            start = mem_slice.start - self._memory_segment_offset

        if mem_slice.stop is not None:
            end = mem_slice.stop - self._memory_segment_offset

        adjusted_slice = slice(start, end)
        return self._memory[adjusted_slice]


    def service(self):
        """
        Emulate the debug service.
        """

        num_gen_registers = self._debugger.get_arch_conf("general_regs")
        endian = self._debugger.get_arch_conf("endian")
        mem_list_fmt = self._debugger.get_arch_conf("mem_list_fmt")

        # register_list_fmt is an array specifying the order register keys are returned by
        # the 'registers' command. The key "general_regs" is expanded to all the r0...rN
        # general registers.
        register_list_fmt = self._debugger.get_arch_conf("register_list_fmt")
        register_order = []
        for reg_name in register_list_fmt:
            if reg_name == "general_regs":
                # Add all general registers to the list here.
                for i in range(0, num_gen_registers):
                    register_order.append(f'r{i}')
            else:
                register_order.append(reg_name)  # Append register name as-is.

        while self.stay_alive:
            while not self._conn.available():
                time.sleep(0.05)  # Sleep for 50ms if no data available.
                if not self.stay_alive:
                    return  # time to leave

            cmdline = self._conn.readline()
            if not len(cmdline):
                continue
            # print(f"Received: {cmdline}")

            cmd = f'{chr(cmdline[0])}'
            args = self._to_args(cmdline[1:])

            if cmd == protocol.DBG_OP_RAMADDR:
                size = args[0]
                addr = args[1]
                data = int.from_bytes(self._get_ram(slice(addr, addr+size)), byteorder=endian)
                self._send(f'{data:x}')
            elif cmd == protocol.DBG_OP_STACKREL:
                SP = self._regs["SP"]
                size = args[0]
                offset = args[1]
                data = int.from_bytes(self._get_ram(slice(SP + offset, SP + offset + size)),
                                      byteorder=endian)
                self._send(f'{data:x}')
            elif cmd == protocol.DBG_OP_BREAK:
                # We're always paused.
                self._send(f'{protocol.DBG_PAUSE_MSG} {debugger.HOST_MAX_PROTOCOL_VERSION:x} 0 0 0')
            elif cmd == protocol.DBG_OP_CONTINUE:
                self._send_comment("Cannot continue in image debugger")
                # Debugger expects a RESULT_ONELINE, so send a formal response that is not
                # 'Continuing' in addition to the user-helpful comment above.
                self._send("error")
            elif cmd == protocol.DBG_OP_ARCH_SPEC:
                # Debugger expects RESULT_LIST operation. Report the arch specs snapshot gathered at
                # dump time.
                for line in self._arch_specs:
                    self._send(line.strip())
                self._send(protocol.DBG_END_LIST)
            elif cmd == protocol.DBG_OP_DEBUGCTL:
                # (note: debug response protocol for this command is undefined)
                self._send_comment("Image debugger does not recognize DEBUGCTL sentences.")
            elif cmd == protocol.DBG_OP_STEP:
                # This is a RESULT_SILENT operation so no formal response required, just a log msg.
                self._send_comment("Cannot step in image debugger")
            elif cmd == protocol.DBG_OP_SET_FLAG:
                # Used to enable/disable breakpoints; unnecessary in static image debugger.
                self._send_comment("Cannot set bit flag in image debugger")
            elif cmd == protocol.DBG_OP_FLASHADDR:
                size = args[0]
                addr = args[1]
                data = int.from_bytes(self._debugger.get_image_bytes(addr, size), byteorder=endian)
                self._send(f'{data:x}')
            elif cmd == protocol.DBG_OP_POKE:
                size = args[0]
                addr = args[1]
                val = args[2]
                new_bytes = val.to_bytes(size, byteorder=endian)
                addr -= self._memory_segment_offset
                for i in range(0, size):
                    self._memory[addr + i] = new_bytes[i]
            elif cmd == protocol.DBG_OP_MEMSTATS:
                if self._memstats is not None:
                    # We memorized memstats during dump process.
                    for key in mem_list_fmt:
                        self._send(f'{self._memstats[key]:x}')
                else:
                    # Don't know the memstats; just send the correct number of 0's.
                    for key in mem_list_fmt:
                        if key == "SP":
                            self._send(f'{self._regs["SP"]:x}')
                        else:
                            self._send('0')  # e.g. unknown __malloc_heap_end
                self._send(protocol.DBG_END_LIST)
            elif cmd == protocol.DBG_OP_PORT_IN:
                # Return a GPIO value to the user.
                addr = args[0]
                try:
                    val = 1 * (self._gpio[addr] != 0)
                except Exception:
                    val = 0  # Invalid GPIO port? Return LOW.
                self._send(f'{int(val)&1:b}')
            elif cmd == protocol.DBG_OP_PORT_OUT:
                # "Drive" a "pin" with the specified GPIO value.
                addr = args[0]
                val = int((args[1] != 0) * 1)
                try:
                    self._gpio[addr] = val
                except Exception:
                    pass  # Invalid GPIO port? Ignore...
            elif cmd == protocol.DBG_OP_RESET:
                self._send_comment("Cannot reset in image debugger")
                # Command does not expect any real response so no more to do here.
            elif cmd == protocol.DBG_OP_REGISTERS:
                for reg_nm in register_order:
                    reg_val = self._regs[reg_nm]
                    self._send(f'{reg_val:x}')
                self._send(protocol.DBG_END_LIST)
            elif cmd == protocol.DBG_OP_TIME:
                # The 'time' is always 0.
                self._send("0")
            else:
                self._send_comment(f"Unknown cmd symbol: '${cmd}'")


    # Private helper methods for the main service.


    def _send(self, text):
        if text[-1] != '\n':
            text = text + "\n"
        # print(f'Sending: {text.encode("UTF-8")}')
        self._conn.write(text.encode("UTF-8"))

    def _send_comment(self, comment):
        self._send(protocol.DBG_RET_PRINT + comment)

    def _to_args(self, line):
        """
        Convert the input line to a list of number arguments
        """
        return [int(token) for token in line.strip().split()]

