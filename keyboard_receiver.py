import json
import sys
import kernel0d as zd
import tty
import termios
import traceback


def read_single_character ():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    tty.setraw(fd)
    ch = sys.stdin.buffer.read(1)
    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def handler (eh,mev):
    print (f'>>> kbd /{mev.port}/ inq#{len(eh.inq)}', file = sys.stderr)
    if mev.port == '':
        ch = read_single_character ()
        if ch:
            zd.send (eh, "", ch.decode (), mev)
    elif mev.port == 'quit':
        print (f'quitting', file=sys.stderr)
        zd.set_idle (eh)    

def reset_handler (eh):
    pass

def instantiate (reg,owner,name, arg, template_data):
    name_with_id = zd.gensymbol ( "keyboard receiver")
    self = None
    eh = zd.make_leaf ( name_with_id, owner, self, arg, handler, reset_handler)
    zd.set_active (eh)
    return eh

# define template
def install (reg):
    zd.register_component (reg, zd.mkTemplate ("keyboard receiver", None, instantiate))


