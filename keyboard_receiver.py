import json
import sys
import kernel0d as zd
import tty
import termios

def handler (eh,mev):
    print (f'handler: /{mev.port}/ /{mev.datum.v}/', file=sys.stderr)
    try:
        if mev.port == '':
            ch = sys.stdin.buffer.read(1)
            print (f'ch: /{str(ch)}/', file=sys.stderr)
            if ch:
                if ch == b'\x03':
                    sys.exit (0)
                zd.send (eh, "", str (ch), mev)
    except (e):
        zd.send (eh, "✗", f"*** error in input_io.py *** {e}", mev)

        
def reset_handler (eh):
    fd = sys.stdin.fileno()
    tty.setraw(fd)

def instantiate (reg,owner,name, arg, template_data):
    fd = sys.stdin.fileno()
    tty.setraw(fd)
    name_with_id = zd.gensymbol ( "keyboard receiver")
    self = None
    eh = zd.make_leaf ( name_with_id, owner, self, arg, handler, reset_handler)
    zd.set_active (eh)
    return eh

# define template
def install (reg):
    zd.register_component (reg, zd.mkTemplate ("keyboard receiver", None, instantiate))


