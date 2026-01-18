import sys
import os
import time
sys.path.insert(0, './pbp/kernel')
import kernel0d as zd
import json

class Ball:
    def __init__(self, initial_x, initial_y, initial_color, initial_dir):
        self.x = initial_x
        self.y = initial_y
        self.color = initial_color
        self.dir = initial_dir
        
class WH:
    def __init__(self):
        self.balls = []
        self.paddle_x = 0
        self.paddle_y = 50
        self.width = None
        self.height = None
        self.state = 'idle'
        self.step_size = None

def handler (eh,mev):
    self = eh.instance_data
    try:
        if 'width' == mev.port:
            self.width = int (mev.datum.v)
            self.step_size = 19
            zd.send (eh, "step size", str (self.step_size), mev)
        elif 'height' == mev.port:
            self.height = int (mev.datum.v)
        elif 'rev' == mev.port:
            self.balls [0].dir = -1 * self.balls [0].dir
            self.balls [0].x = self.balls [0].x + (self.balls [0].dir * self.step_size)
        elif '' == mev.port:
            if self.state == 'idle':
                ball1 = Ball (0, 100, "#ffff00", 1)
                self.balls = [ ball1 ]
                # send paddle image if first time
                zd.send (eh, "", '{' + f'"type":"paddle","id":"left","x":{self.paddle_x},"y":{self.paddle_y}' + '}', mev)
                zd.send (eh, "x", f'{ball1.x}' , mev)
                self.state = 'looping'
            self.balls [0].x = self.balls[0].x + (self.balls [0].dir * self.step_size)
            ballpositions = []
            for ball in self.balls:
                ballpositions.append ({"type": "ball", "x" : ball.x, "y" : ball.y, "color": ball.color})
            zd.send (eh, "", json.dumps (ballpositions), mev)
            zd.send (eh, "x", f'{self.balls [0].x}' , mev)
        else:
             zd.send (eh, "✗", f"unrecognized port '{mev.port}' in test.py", mev)
    except Exception as err:
        zd.send (eh, "✗", f"*** error in test.py *** {err}", mev)
        
def instantiate (reg,owner,name, arg, template_data):
    name_with_id = zd.gensymbol ( "Test")
    self = WH ()
    return zd.make_leaf ( name_with_id, owner, self, arg, handler)

# define template
def install (reg):
    zd.register_component (reg, zd.mkTemplate ("Test", None, instantiate))


