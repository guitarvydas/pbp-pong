import sys
import time
sys.path.insert(0, './pbp/kernel')
import kernel0d as zd

class Flags:
    def __init__ (self):
        self.a = False
        self.b = False

def handler (eh,mev):
    self = eh.instance_data
    def MaybeAck ():
        if self.a and self.b:
            zd.send (eh, "", "", mev)
            self.a = False
            self.b = False
    match mev.port:
        case "1": self.a = True ; MaybeAck ()
        case "2": self.b = True ; MaybeAck ()
        case   _: raise Exception (f'internal failure in Both port="{mev.port}" payload="{mev.datum.v}"')
        
def instantiate (reg,owner,name, arg, template_data):
    name_with_id = zd.gensymbol ( "Both")
    self = Flags ()
    return zd.make_leaf ( name_with_id, owner, self, arg, handler)

# define template
def install (reg):
    zd.register_component (reg, zd.mkTemplate ("Both", None, instantiate))


