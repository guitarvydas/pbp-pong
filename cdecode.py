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
    elif mev.datum.v == 'p':
        zd.send (eh, "rightup", "", mev)
    elif mev.datum.v == ';':
        zd.send (eh, "rightdown", "", mev)

    elif mev.datum.v == 'z':
        zd.send (eh, "ltoggle", "", mev)
    elif mev.datum.v == '/':
        zd.send (eh, "rtoggle", "", mev)

    elif mev.datum.v == 'h':
        zd.send (eh, "bleft", "", mev)
    elif mev.datum.v == 'j':
        zd.send (eh, "bdown", "", mev)
    elif mev.datum.v == 'k':
        zd.send (eh, "bup", "", mev)
    elif mev.datum.v == 'l':
        zd.send (eh, "bright", "", mev)

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


