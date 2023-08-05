# (c) Copyright 2022 Aaron Kimball

import arduino_dbg.term as term

DBG_CONF_FMT_VERSION = 1


def load_config_file(print_q, filename, map_name='config', defaults=None):
    """
    Read a debugger configuration file map.
    This is actually a python file that will be evaluated in a sterile environment.
    It should contain two variables afterward:
    - `formatversion` specifies this serialization version
    - `{map_name}` is a dict of k-v pairs.

    If `defaults` is a map, then its values populate anything omitted from the loaded map.

    TODO(aaron): This is insecure.
    """
    if defaults is None:
        defaults = {}
    new_conf = defaults.copy()

    # The loaded config will be a map named '{map_name}' within an otherwise-empty environment
    init_env = {}
    init_env[map_name] = {}

    with open(filename, "r") as f:
        conf_text = f.read()
        try:
            exec(conf_text, init_env, init_env)
        except BaseException:
            # Error parsing or executing the config file.
            # Catch BaseException to prevent e.g. sys.exit() triggers from within conf file.
            print_q.put((("Warning: error parsing config file '%s'" % filename), term.MsgLevel.WARN))
            init_env[map_name] = {}
            init_env['formatversion'] = DBG_CONF_FMT_VERSION

    try:
        fmtver = init_env['formatversion']
        if not isinstance(fmtver, int) or fmtver > DBG_CONF_FMT_VERSION:
            print_q.put(
                (f"Error: Cannot read config file '{filename}' with version {fmtver}", term.MsgLevel.ERR))
            init_env[map_name] = {}  # Disregard the unsupported configuration data.

        loaded_conf = init_env[map_name]
    except Exception:
        print_q.put((f"Error in format for config file '{filename}'", term.MsgLevel.ERR))
        loaded_conf = {}

    # Merge loaded data on top of our default config.
    for (k, v) in loaded_conf.items():
        new_conf[k] = v

    return new_conf


MAX_BYTES_PER_LINE = 40


def __persist_conf_var(f, k, v):
    """
    Persist k=v in serialized form to the file handle 'f'.

    Can be called with k=None to serialize a nested value in a complex type.
    """

    if k is not None:
        f.write(f'  {repr(k)}: ')

    if v is None or type(v) == str or type(v) == int or type(v) == float or type(v) == bool:
        f.write(repr(v))
    elif type(v) == bytes or type(v) == bytearray:
        vbytes = bytes(v)
        length = len(vbytes)
        if length > MAX_BYTES_PER_LINE:
            # This is used for things like memory dumps; don't create a giant multi-KB line,
            # it tends to be hard to work with if we need to inspect the file. Chop it up.
            first = True
            for offset in range(0, length, MAX_BYTES_PER_LINE):
                if not first:
                    f.write(' + \\\n    ')
                f.write(repr(vbytes[offset: offset + MAX_BYTES_PER_LINE]))
                first = False
        else:
            f.write(repr(bytes(v)))
    elif type(v) == list:
        f.write('[')
        for elem in v:
            __persist_conf_var(f, None, elem)
            f.write(", ")
        f.write(']')
    elif type(v) == dict:
        f.write("{\n")
        for (dirK, dirV) in v.items():
            f.write('    ')
            __persist_conf_var(f, None, dirK)  # keys in a dir can be any type, not just str
            f.write(": ")
            __persist_conf_var(f, None, dirV)
            f.write(",\n")
        f.write("  }")
    else:
        print("Warning: unknown type serialization '%s'" % str(type(v)))
        # Serialize it as an abstract map; filter out python internals and methods
        objdir = dict(
            [(dirK, dirV) for (dirK, dirV) in dir(v).items() if
             (not dirK.startswith("__") and not dirK.endswith("__") and not callable(getattr(v, dirK)))])

        __persist_conf_var(f, None, objdir)

    if k is not None:
        f.write(",\n")


def persist_config_file(filename, map_name, data):
    """
    Write configuration information out to a file.
    """

    with open(filename, "w") as f:
        f.write(f"formatversion = {DBG_CONF_FMT_VERSION}\n")
        f.write(f"{map_name} = {{\n\n")
        for (k, v) in data.items():
            __persist_conf_var(f, k, v)
        f.write("\n}\n")

