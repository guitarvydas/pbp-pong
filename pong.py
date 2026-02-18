import json
import sys
import kernel0d as zd

paddle_inc = 0.03
left_paddle_y = 0.5
right_paddle_y = 0.5

def handler (eh,mev):
    global paddle_inc, left_paddle_y, right_paddle_y
    if mev.port == '':
        if ch:
            zd.send (eh, "", str (ch), mev)
        
def reset_handler (eh):
    pass

def instantiate (reg,owner,name, arg, template_data):
    name_with_id = zd.gensymbol ( "pong")
    self = None
    eh = zd.make_leaf ( name_with_id, owner, self, arg, handler, reset_handler)
    zd.set_active (eh)
    return eh

# define template
def install (reg):
    zd.register_component (reg, zd.mkTemplate ("pong", None, instantiate))


