import sys
import kernel0d as zd

import io
import termios

import keyboard_receiver
import pong
import notquit

###
fd = None
old_settings = None

def keyboard_init ():
    global fd, old_settings
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)

def keyboard_reset ():
    global fd, old_settings
    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

###

keyboard_init ()
[palette, env] = zd.initialize_from_files (sys.argv[3:])
keyboard_receiver.install (palette)
pong.install (palette)
notquit.install (palette)
top = zd.start_bare (part_name=sys.argv[2], palette=palette, env=env)
zd.inject (top, "", sys.argv[1])
zd.finalize (top)
keyboard_reset ()





