import sys
sys.path.insert(0, './pbp/kernel')
import kernel0d as zd

class Counter:
    def __init__ (self):
        self.count = 0
    def inc (self):
        self.count +=1
    def done (self):
        return (self.count >= 10)
    def reset (self):
        self.count = 0

def handler (eh,mev):
    self = eh.instance_data
    try:
        self = eh.instance_data
        if self.done ():
            self.reset ()
        else:
            self.inc ()
            zd.send (eh, "", f'{self.count}', mev)
    except (etentimes):
        zd.send (eh, "✗", f"*** error in Tentimes.py *** {etentimes}", mev)
        
def instantiate (reg,owner,name, arg, template_data):
    name_with_id = zd.gensymbol ( "TenTimes")
    self = Counter ()
    return zd.make_leaf ( name_with_id, owner, self, arg, handler)

# define template
def install (reg):
    zd.register_component (reg, zd.mkTemplate ("TenTimes", None, instantiate))


