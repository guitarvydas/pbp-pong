import json
import sys
import kernel0d as zd

# ANSI escape sequences for arrow keys
UP_ARROW = b'\x1b[A'
DOWN_ARROW = b'\x1b[B'

def handler (eh,mev):
    try:
        if mev.port == '':
            key = mev.datum.v
            # translate ANSI key sequences into pulses on the appropriate output ports, "up" and "down", else remain silent
            if key == UP_ARROW:
                zd.send (eh, "up", "", mev)
            elif key == DOWN_ARROW:
                zd.send (eh, "down", "", mev)
            else:
                pass
    except (e):
        zd.send (eh, "✗", f"*** error in key_decoder.py *** {e}", mev)

        
def instantiate (reg,owner,name, arg, template_data):
    name_with_id = zd.gensymbol ( "Key Decoder")
    self = None
    return zd.make_leaf ( name_with_id, owner, self, arg, handler)

# define template
def install (reg):
    zd.register_component (reg, zd.mkTemplate ("Key Decoder", None, instantiate))


