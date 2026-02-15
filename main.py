import sys
import kernel0d as zd

import io
import keyboard_receiver
import termios

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

[palette, env] = zd.initialize_from_files (sys.argv[3:])
keyboard_receiver.install (palette)
initialize_keyboard ()
try:
    top = zd.start_bare (part_name=sys.argv[2], palette=palette, env=env)
    zd.inject (top, "", sys.argv[1])
    zd.finalize (top)
finally:
    reset_keyboard ()





