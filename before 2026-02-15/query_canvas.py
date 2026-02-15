import sys
sys.path.insert(0, './pbp/kernel')
import kernel0d as zd
import json

def handler (eh,mev):
    print (mev, file=sys.stderr)
    print (f'port=/{mev.port}/', file=sys.stderr)
    print (f'datum=/{mev.datum}', file=sys.stderr)
    print (f'v=/{mev.datum.v}/', file=sys.stderr)
    self = eh.instance_data
    port = mev.port
    v    = mev.datum.v
    try:
        obj = json.loads(v)
        zd.send (eh, "width", obj['width'], mev)
        zd.send (eh, "height", obj['height'], mev)
    except (qerr):
        zd.send (eh, "✗", f"*** error in query_canvas.py *** {qerr}", mev)

def instantiate (reg,owner,name, arg, template_data):
    name_with_id = zd.gensymbol ( "Query Canvas")
    self = None
    return zd.make_leaf ( name_with_id, owner, self, arg, handler)

# define template
def install (reg):
    zd.register_component (reg, zd.mkTemplate ("Query Canvas", None, instantiate))


