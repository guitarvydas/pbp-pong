import sys
import kernel0d as zd

try:

    # initialize palette of parts and environment for the kernel (names of Container parts on diagram, along with command line arg)
    [palette, env] = zd.initialize_component_palette_from_files (sys.argv[1], sys.argv[4:])
    # begin running the part
    part = zd.start_bare (arg=sys.argv[2], Part_name=sys.argv[3], palette=palette, env=env)

    # inject False on both input ports A and B
    part.inject ("A", "") # empty string payload is converted to False
    part.inject ("B", "") # empty string payload is converted to False

    # show output queue of part as JSON array of mevents (key/value pairs in order that they were generated)
    part.finalize ()

except Exception as e:
    _, _, tb = sys.exc_info()
    while tb.tb_next:
        tb = tb.tb_next
    frame = tb.tb_frame
    filename = frame.f_code.co_filename
    line_number = tb.tb_lineno
    print(f"\n\n\n*** {type(e).__name__} at {filename}:{line_number}: {e}", file=sys.stderr)

