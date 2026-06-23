import sys
import kernel0d as zd

import andgate

[palette, env] = zd.initialize_from_files (sys.argv[3:])
andgate.install (palette)
top = zd.start_bare (part_name=sys.argv[2], palette=palette, env=env)
zd.inject (top, "A", "")
zd.inject (top, "B", "")
zd.finalize (top)

