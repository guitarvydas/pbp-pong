import sys
sys.path.insert(0, './pbp/kernel')
import kernel0d as zd

def handler (eh,mev):
    try:
        if '' == mev.datum.v:
            zd.send (eh, "", '[{"type":"ball","x":150,"y":310,"color":"#ff00ff"},{"type":"paddle","id":"left","x":50,"y":250}]', mev)
        else:
            print (f'test: {mev.datum.v}', file=sys.stderr)
            x = int(mev.datum.v) * 10
            zd.send (eh, "", "{" + f'"type":"ball","x":"{x}","y":"310","color":"#ff00ff"' + "}" , mev)
    except (testerr):
        zd.send (eh, "✗", f"*** error in Test.py *** {testerr}", mev)
        
def instantiate (reg,owner,name, arg, template_data):
    name_with_id = zd.gensymbol ( "Test")
    return zd.make_leaf ( name_with_id, owner, None, arg, handler)

# define template
def install (reg):
    zd.register_component (reg, zd.mkTemplate ("Test", None, instantiate))


