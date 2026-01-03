import sys
sys.path.insert(0, './pbp/kernel')
import kernel0d as zd

def handler (eh,mev):
    try:
        zd.send (eh, "", '[{"type":"ball","x":150,"y":310,"color":"#ff00ff"},{"type":"paddle","id":"left","x":50,"y":250}]', mev)
    except (e):
        zd.send (eh, "✗", "*** error in Test.py ***", mev)
        
def instantiate (reg,owner,name, arg, template_data):
    name_with_id = zd.gensymbol ( "Test")
    return zd.make_leaf ( name_with_id, owner, None, arg, handler)

# define template
def install (reg):
    zd.register_component (reg, zd.mkTemplate ("Test", None, instantiate))


