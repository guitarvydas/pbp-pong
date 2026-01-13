import sys
import time
sys.path.insert(0, './pbp/kernel')
import kernel0d as zd

def handler (eh,mev):
    try:
        if '' == mev.port:
            zd.send (eh, "", '[{"type":"ball","x":150,"y":310,"color":"#ffff00"},{"type":"paddle","id":"left","x":50,"y":250}]', mev)
        elif 'size' == mev.port:
            print (f'size={mev.datum.v}', file=sys.stderr)
        else:
            x = int(mev.datum.v) * 10
            zd.send (eh, "", "{" + f'"type":"ball","x":"{x}","y":"310","color":"#00ff00"' + "}" , mev)
    except (testerr):
        zd.send (eh, "✗", f"*** error in Test.py *** {testerr}", mev)
        
def instantiate (reg,owner,name, arg, template_data):
    name_with_id = zd.gensymbol ( "Test")
    return zd.make_leaf ( name_with_id, owner, None, arg, handler)

# define template
def install (reg):
    zd.register_component (reg, zd.mkTemplate ("Test", None, instantiate))


