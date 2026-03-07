import json
import sys
import kernel0d as zd

paddle_inc = 0.03
left_paddle_y = 0.5
right_paddle_y = 0.5

ballx = 0.5
bally = 0.7
ball_inc = 0.03

def handler (eh,mev):
    global paddle_inc, left_paddle_y, right_paddle_y
    global ballx, bally, ball_inc
    if mev.port == 'lup':
        left_paddle_y += paddle_inc
        cmd = f'{{"type":"paddle","id":"left","y":{left_paddle_y}}}'
        zd.send (eh, "gui", cmd, mev)
        zd.send (eh, "more", "", mev)
    elif mev.port == 'ldown':
        left_paddle_y -= paddle_inc
        cmd = f'{{"type":"paddle","id":"left","y":{left_paddle_y}}}'
        zd.send (eh, "gui", cmd, mev)
        zd.send (eh, "more", "", mev)
    elif mev.port == 'rup':
        right_paddle_y += paddle_inc
        cmd = f'{{"type":"paddle","id":"right","y":{right_paddle_y}}}'
        zd.send (eh, "gui", cmd, mev)
        zd.send (eh, "more", "", mev)
    elif mev.port == 'rdown':
        right_paddle_y -= paddle_inc
        cmd = f'{{"type":"paddle","id":"right","y":{right_paddle_y}}}'
        zd.send (eh, "gui", cmd, mev)
        zd.send (eh, "more", "", mev)

    elif mev.port == 'bdown':
        bally -= ball_inc
        cmd = f'{{"type":"ball","x":"{ballx}","y":{bally}}}'
        zd.send (eh, "gui", cmd, mev)
        zd.send (eh, "more", "", mev)
    elif mev.port == 'bup':
        bally += ball_inc
        cmd = f'{{"type":"ball","x":"{ballx}","y":{bally}}}'
        zd.send (eh, "gui", cmd, mev)
        zd.send (eh, "more", "", mev)
    elif mev.port == 'bright':
        ballx += ball_inc
        cmd = f'{{"type":"ball","x":"{ballx}","y":{bally}}}'
        zd.send (eh, "gui", cmd, mev)
        zd.send (eh, "more", "", mev)
    elif mev.port == 'bleft':
        ballx -= ball_inc
        cmd = f'{{"type":"ball","x":"{ballx}","y":{bally}}}'
        zd.send (eh, "gui", cmd, mev)
        zd.send (eh, "more", "", mev)

    elif mev.port == 'other':
        zd.send (eh, "more", "", mev)
    elif mev.port == 'quit':
        zd.send (eh, "quit", "", mev)
    elif mev.port == "init":
        zd.send (eh, "gui", f'{{"type":"paddle","id":"left","y":{left_paddle_y}}}', mev)
        zd.send (eh, "gui", f'{{"type":"paddle","id":"right","y":{right_paddle_y}}}', mev)
        zd.send (eh, "gui", f'{{"type":"ball","x":{ballx},"y":{bally}}}', mev)
        zd.send (eh, "more", "", mev)
    else:
        pass
    
def reset_handler (eh):
    pass

def instantiate (reg,owner,name, arg, template_data):
    name_with_id = zd.gensymbol ( "pong")
    self = None
    eh = zd.make_leaf ( name_with_id, owner, self, arg, handler, reset_handler)
    return eh

# define template
def install (reg):
    zd.register_component (reg, zd.mkTemplate ("pong", None, instantiate))


