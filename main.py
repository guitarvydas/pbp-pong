import sys
sys.path.insert(0, './pbp/kernel')
import kernel0d as zd

import test
import tentimes
import getsize

[palette, env] = zd.initialize_from_files (sys.argv[1], sys.argv[4:])
test.install (palette)
tentimes.install (palette)
getsize.install (palette)
top = zd.start_bare (part_name=sys.argv[3], palette=palette, env=env)
zd.inject (top, "", sys.argv[2])
zd.finalize (top)
