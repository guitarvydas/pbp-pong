import sys
import time
sys.path.insert(0, './pbp/kernel')
import kernel0d as zd

def handler (eh,mev):
    zd.forward (eh, "", mev)
    zd.send (eh, "ack", "", mev)
    
def instantiate (reg,owner,name, arg, template_data):
    name_with_id = zd.gensymbol ( "EchoAck")
    return zd.make_leaf ( name_with_id, owner, None, arg, handler)

# define template
def install (reg):
    zd.register_component (reg, zd.mkTemplate ("EchoAck", None, instantiate))


