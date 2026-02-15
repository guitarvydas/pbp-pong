import sys
import kernel0d as zd

def handler (eh,mev):
    try:
        zd.send (eh, "", 'SIZE', mev)
    except (testerr):
        zd.send (eh, "✗", f"*** error in get-size.py *** {testerr}", mev)
        
def instantiate (reg,owner,name, arg, template_data):
    name_with_id = zd.gensymbol ( "Get Canvas Size")
    return zd.make_leaf ( name_with_id, owner, None, arg, handler)

# define template
def install (reg):
    zd.register_component (reg, zd.mkTemplate ("Get Canvas Size", None, instantiate))


