import sys
import kernel0d as zd


class AndGate:
    def __init__ (self):
        self.reset ()
        
    def reset (self):
        self.inA = False
        self.inB = False
        self.out = False
        
    def eval (self, eh, outport, cause):
        self.out = self.inA & self.inB
        zd.send (eh, outport, bool_to_str (self.out), cause)
        
def handler (eh, mev):
    print (f'handler {mev.port}', file=sys.stderr)
    self = eh.instance_data
    if mev.port == "A":
        self.inA = bool (mev.datum.v)
        self.eval (eh, "", mev)
    elif mev.port == "B":
        self.inB = bool (mev.datum.v)
        self.eval (eh, "", mev)

def reset_handler (eh):
    eh.instance_data.reset ()
        
def instantiate (reg, owner, name, arg, template_data):
    name_with_id = zd.gensymbol ("AndGate")
    self = AndGate ()
    return zd.make_leaf (name_with_id, owner, self, arg, handler, reset_handler)

def install (reg):
    zd.register_component (reg, zd.mkTemplate ("AndGate", None, instantiate))
    
        

def bool_to_str(b):
    return "1" if b else ""
