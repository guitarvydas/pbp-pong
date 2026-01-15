import json
import sys
sys.path.insert(0, './pbp/kernel')
import kernel0d as zd

class WH:
    def __init__(self):
        self.x = 0
        self.y = 310
        self.width = None
        self.height = None

def handler (eh,mev):
    try:
        self = eh.instance_data
        print (f'wh: port={mev.port} payload={mev.datum.v} int(payload)={int(mev.datum.v)}')
        if mev.port == 'width':
            self.width = int (mev.datum.v) ## just save the value
        elif mev.port == '':
            x = int (mev.datum.v)
            if x <= 0:
                zd.send (eh, "rev", "", mev)
            elif x >= self.width:
                zd.send (eh, "rev", "", mev)
            else:
                pass
            zd.send (eh, "", mev.datum.v, mev) ## send a trigger to keep running the loop
        else:
            raise ValueError(f"unrecognized port {mev.port}")
    except (e):
        zd.send (eh, "✗", f"*** error in looptest.py *** {e}", mev)
        
def instantiate (reg,owner,name, arg, template_data):
    name_with_id = zd.gensymbol ( "Loop Test")
    self = WH ()
    return zd.make_leaf ( name_with_id, owner, self, arg, handler)

# define template
def install (reg):
    zd.register_component (reg, zd.mkTemplate ("Loop Test", None, instantiate))


