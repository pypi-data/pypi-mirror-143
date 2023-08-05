# (c) Copyright 2021 Aaron Kimball
#
# Methods that pipe out to programs included in gnu binutils
# (c++filt, addr2line).

import locale
import queue
import re
import subprocess
import threading

import arduino_dbg.term as term


# undesirable suffixes on demangled names
_clone_regex = re.compile(r'\[clone \.[A-Za-z_]+.*\]$')


class DemangleThread(threading.Thread):
    """
    Thread that communicates with a long-running `c++filt(1)` instance to demangle
    C++ names. As overhead from repeatedly invoking this program in a subprocess
    causes significant lag when parsing debug info, we open a single long-lived
    instance and pass names one-by-one.
    """
    def __init__(self, hide_params, print_q):
        super().__init__(name=f'DemangleThread({hide_params})', daemon=True)
        self.hide_params = hide_params
        self._print_q = print_q

        self._in_q = queue.Queue(maxsize=1)  # Queues to communicate w/ main thread
        self._out_q = queue.Queue(maxsize=1)

        # Requests to demangle can only be made if you hold the lock.
        self._user_lock = threading.Lock()

        self._start_process()

        self._running = True
        self.start()

    def __repr__(self):
        return f"DemangleThread(hide_params={self.hide_params})"

    def _start_process(self):
        """
        Start the c++filt instance.
        """
        args = ['c++filt']
        if self.hide_params:
            args.append('-p')  # Suppress method arguments in output.

        self.proc = subprocess.Popen(args,
                                     stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=None,
                                     encoding=locale.getpreferredencoding(),
                                     close_fds=True)

    def close(self):
        """
        Shut down the demangle thread process.
        """
        if not self._running:
            # Don't submit to a queue to a thread that's no longer active.
            self.join()
            return

        self._user_lock.acquire()
        try:
            self._running = False
            self._in_q.put(None)  # Bounce the loop to detect _running == False condition.
            self._in_q.join()
            self.join()
        finally:
            self._user_lock.release()

    def run(self):
        """
        Interact with an instance of `c++filt` running as a subprocess.
        """
        name = None
        demangled = None
        try:
            while self._running:
                name = self._in_q.get()
                try:
                    if name is None:
                        continue

                    if self.proc.poll() is not None:
                        # The c++filt instance closed itself. Restart it.
                        self._start_process()

                    # Send a (mangled) name to c++filt on stdin. Get the response line,
                    # which is the demangled form; return that to the out_q.
                    try:
                        self.proc.stdin.write(f'{str(name).strip()}\n')
                        self.proc.stdin.flush()
                    except Exception as e:
                        self._print_q.put((f'Exception on STDIN in {repr(self)}: {e}', term.ERR))
                        self._print_q.put((f'Last input to demangler: "{name}"', term.ERR))
                        raise

                    try:
                        demangled = self.proc.stdout.readline()
                    except Exception as e:
                        self._print_q.put((f'Exception on STDOUT in {repr(self)}: {e}', term.ERR))
                        self._print_q.put((f'Last input to demangler: "{name}"', term.ERR))
                        raise
                finally:
                    self._in_q.task_done()  # Acknowledge task-complete condition.

                if demangled is None:
                    demangled = ''

                demangled = demangled.strip()
                self._out_q.put(demangled)
        except Exception as e:
            self._print_q.put((f'Exception in {repr(self)}: {e}', term.ERR))
            self._print_q.put((f'Last input to demangler: "{name}"', term.ERR))
            self._print_q.put((f'Last demangler output: "{demangled}"', term.ERR))
        finally:
            # No matter how we got here (normal shutdown or exception) mark the thread as done.
            self._running = False

            # Close the pipe.
            try:
                self.proc.stdin.close()  # Should cause the subprocess to stop.
            except Exception:
                pass

            try:
                self.proc.wait()  # Wait for subprocess completion.
            except Exception:
                pass

            try:
                self.proc.stdout.close()
            except Exception:
                pass


    def demangle(self, name):
        """
        Send `name` to c++filt for demangling; return the demangled name.
        """
        if not self._running:
            raise Exception(f"Demangler thread ({self}) has shut down")

        acquired = self._user_lock.acquire(blocking=True)
        if not acquired:
            raise Exception("Could not lock demangler thread.")
        try:
            self._in_q.put(name)
            self._in_q.join()
            demangled = self._out_q.get()
            self._out_q.task_done()  # Acknowledge receipt.

        finally:
            self._user_lock.release()

        return demangled


# Global instances of DemangleThread; used within demangle()
_main_demangle_thread = None
_hide_param_demangle_thread = None


def close_demangle_threads():
    """
    Close global DemangleThread instances.
    """
    global _main_demangle_thread, _hide_param_demangle_thread

    try:
        if _main_demangle_thread is not None:
            _main_demangle_thread.close()
    except Exception:
        pass

    try:
        if _hide_param_demangle_thread is not None:
            _hide_param_demangle_thread.close()
    except Exception:
        pass

    _main_demangle_thread = None
    _hide_param_demangle_thread = None


def start_demangle_threads(print_q):
    """
    Bootstrap global DemangleThread instances.
    """
    global _main_demangle_thread, _hide_param_demangle_thread

    if _hide_param_demangle_thread is None:
        _hide_param_demangle_thread = DemangleThread(hide_params=True, print_q=print_q)

    if _main_demangle_thread is None:
        _main_demangle_thread = DemangleThread(hide_params=False, print_q=print_q)


def demangle(name, hide_params=False):
    """
        Use c++filt in binutils to demangle a C++ name into a human-readable one.
        @
    """
    if name is None:
        return None
    elif name == '':
        return ''

    global _hide_param_demangle_thread, _main_demangle_thread
    if hide_params:
        demangle_thread = _hide_param_demangle_thread
    else:
        demangle_thread = _main_demangle_thread

    demangled = demangle_thread.demangle(name)

    # Remove any '[clone .constprop.NN]', etc suffixes.
    demangled = _clone_regex.sub('', demangled)

    # print(f"Demangled: {name} -> {demangled}")
    return demangled


def pc_to_source_line(elf_file, addr):
    """
        Given a program counter ($PC) value, establish what line of source it comes from.
    """
    if addr is None:
        return None
    args = ["addr2line", "-s", "-e", elf_file, ("%x" % addr)]
    pipe = subprocess.Popen(args, stdin=None, stdout=subprocess.PIPE,
                            encoding=locale.getpreferredencoding())
    stdout, _ = pipe.communicate()
    source_lines = stdout.split("\n")
    src_line = source_lines[0]
    if src_line.startswith("??:"):
        return None
    return src_line

