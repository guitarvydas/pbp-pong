import json
import sys
import kernel0d as zd

def handler (eh,mev):
    if mev.datum.v == '\x03':
        zd.send (eh, "quit", "", mev)
    elif mev.datum.v == 'q':
        zd.send (eh, "leftup", "", mev)
    elif mev.datum.v == 'a':
        zd.send (eh, "leftdown", "", mev)
    else:
        pass
    
def reset_handler (eh):
    pass

def instantiate (reg,owner,name, arg, template_data):
    name_with_id = zd.gensymbol ( "cdecode")
    self = None
    eh = zd.make_leaf ( name_with_id, owner, self, arg, handler, reset_handler)
    return eh

# define template
def install (reg):
    zd.register_component (reg, zd.mkTemplate ("cdecode", None, instantiate))


