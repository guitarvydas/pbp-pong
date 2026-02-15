import json
import sys
import kernel0d as zd
import tty
import termios

def handler (eh,mev):
    try:
        if mev.port == '':
            zd.set_active (eh)
            ch = sys.stdin.buffer.read(1)
            if ch:
                zd.send (eh, "", str (ch), mev)
    except (e):
        zd.send (eh, "✗", f"*** error in input_io.py *** {e}", mev)

        
def instantiate (reg,owner,name, arg, template_data):
    tty.setraw(fd)
    name_with_id = zd.gensymbol ( "keyboard receiver")
    self = None
    return zd.make_leaf ( name_with_id, owner, self, arg, handler)

# define template
def install (reg):
    zd.register_component (reg, zd.mkTemplate ("keyboard receiver", None, instantiate))


