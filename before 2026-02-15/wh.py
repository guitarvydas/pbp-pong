import sys
import time
sys.path.insert(0, './pbp/kernel')
import kernel0d as zd

class WH:
    def __init__(self):
        self.width = None
        self.height = None
        
def handler (eh,mev):
    self = eh.instance_data
    try:
        import json
        data = json.loads(mev.datum.v)
        self.width = data["canvas"]["width"]
        self.height = data["canvas"]["height"]
        zd.send (eh, "width", f'{self.width}', mev)
        zd.send (eh, "height", f'{self.height}', mev)
    except Exception as testerr:
        zd.send (eh, "✗", f"*** error in wh.py *** {testerr}", mev)
        
def instantiate (reg,owner,name, arg, template_data):
    name_with_id = zd.gensymbol ( "Width Height")
    self = WH ()
    return zd.make_leaf ( name_with_id, owner, self, arg, handler)

# define template
def install (reg):
    zd.register_component (reg, zd.mkTemplate ("Width Height", None, instantiate))


