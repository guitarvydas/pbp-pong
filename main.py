import sys
import kernel0d as zd

import io
import termios

import keyboard_receiver


### I/O external to PBP ###
fd = None
old_settings = None

def initialize_keyboard ():
    # Save terminal settings and switch to raw mode
    global fd, old_settings
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)

def reset_keyboard ():
    # Restore terminal settings
    global fd, old_settings
    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
### end external ###

print (f'begin', file=sys.stderr)
[palette, env] = zd.initialize_from_files (sys.argv[3:])
print (f'install', file=sys.stderr)
keyboard_receiver.install (palette)
print (f'init kbd', file=sys.stderr)
initialize_keyboard ()
print (f'try', file=sys.stderr)
try:
    top = zd.start_bare (part_name=sys.argv[2], palette=palette, env=env)
    print (f'inject', file=sys.stderr)
    zd.inject (top, "", sys.argv[1])
    print (f'finalize', file=sys.stderr)
    zd.finalize (top)
finally:
    print (f'finally', file=sys.stderr)
    reset_keyboard ()
print (f'done', file=sys.stderr)





