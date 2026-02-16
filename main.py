import sys
import kernel0d as zd

import io
import termios

import keyboard_receiver

###
fd = None
old_settings = None

def keyboard_init ():
    global fd, old_settings
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)

def keyboard_reset ():
    global fd, old_settings
    print (f'keyboard reset', file=sys.stderr)
    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

###

keyboard_init ()
print (f'begin', file=sys.stderr)
[palette, env] = zd.initialize_from_files (sys.argv[3:])
print (f'install', file=sys.stderr)
keyboard_receiver.install (palette)
print (f'init kbd', file=sys.stderr)
print (f'try', file=sys.stderr)
top = zd.start_bare (part_name=sys.argv[2], palette=palette, env=env)
print (f'inject', file=sys.stderr)
zd.inject (top, "", sys.argv[1])
print (f'finalize', file=sys.stderr)
zd.finalize (top)
keyboard_reset ()





