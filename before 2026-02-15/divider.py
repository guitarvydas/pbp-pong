import sys
sys.path.insert(0, './pbp/kernel')
import kernel0d as zd

class Count:
    def __init__ (self):
        self.reset ()
        self.max = 1

    def reset (self):
        self.counter = 0
    def inc (self):
        self.counter += 1
    def reached_limit (self):
        return self.counter >= self.max

def handler (eh,mev):
    self = eh.instance_data
    port = mev.datum.port
    v = mev.datum.v
    try:
        if port == "⟳":
            self.reset ()
        elif port == "tick":
            self.inc ()
            if self.reached_limit () :
                zd.send (eh, "", "", mev)
                self.reset ()
        else:
            zd.send (eh, "✗", "*** bad input to Divider.py ***", mev)
            
    except (e):
        zd.send (eh, "✗", "*** error in Divider.py ***", mev)
        


def instantiate (reg,owner,name, arg, template_data):
    name_with_id = zd.gensymbol ( "Divider")
    self = Count ()
    return zd.make_leaf ( name_with_id, owner, self, arg, handler)

# define template
def install (reg):
    zd.register_component (reg, zd.mkTemplate ("Divider", None, instantiate))


