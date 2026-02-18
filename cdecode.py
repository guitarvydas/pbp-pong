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
    elif mev.datum.v == 'o':
        zd.send (eh, "rightup", "", mev)
    elif mev.datum.v == 'l':
        zd.send (eh, "rightdown", "", mev)
    else:
        zd.send (eh, "other", mev.datum.v, mev)
    
def reset_handler (eh):
    pass

def instantiate (reg,owner,name, arg, template_data):
    name_with_id = zd.gensymbol ( "character decoder")
    self = None
    eh = zd.make_leaf ( name_with_id, owner, self, arg, handler, reset_handler)
    return eh

# define template
def install (reg):
    zd.register_component (reg, zd.mkTemplate ("character decoder", None, instantiate))


