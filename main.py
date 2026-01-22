import sys
sys.path.insert(0, './pbp/kernel')
import kernel0d as zd

import test
import looptest
import getsize
import wh
import kill
import both
import echoack

[palette, env] = zd.initialize_from_files (sys.argv[1], sys.argv[4:])
test.install (palette)
looptest.install (palette)
getsize.install (palette)
wh.install (palette)
kill.install (palette)
both.install (palette)
echoack.install (palette)
top = zd.start_bare (part_name=sys.argv[3], palette=palette, env=env)
zd.inject (top, "", sys.argv[2])
zd.finalize (top)

