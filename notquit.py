import json
import sys
import kernel0d as zd

def handler (eh,mev):
    if mev.datum.v != b'x':
        zd.forward (eh, "", mev)
    else:
        pass
    
def reset_handler (eh):
    pass

def instantiate (reg,owner,name, arg, template_data):
    name_with_id = zd.gensymbol ( "not quit")
    self = None
    eh = zd.make_leaf ( name_with_id, owner, self, arg, handler, reset_handler)
    return eh

# define template
def install (reg):
    zd.register_component (reg, zd.mkTemplate ("not quit", None, instantiate))


