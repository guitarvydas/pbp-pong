import sys
sys.path.insert(0, './pbp/kernel')
import kernel0d as zd

import random

class Point:
    def __init__ (self, x, y):
        self.x = x
        self.y = y

class Ball_State:
    def __init__ (self):
        self.reset ()

    def reset (self):
        # coord (0,0) is in the middle of the display
        #  x is +ve for left-to-right, -ve for right-to-left
        #  y is +ve for upwards, -ve for downwards

        self.xdirection = random.choice (["leftwards", "rightwards"])
        self.ydirection = random.choice (["downwards", "upwards"])

        self.location = Point (0, self.scale (random.random ())) # x,y both floats between 0 and 1

        # vector is a unit vector
        ydir = 1
        xdir = 1
        if self.xdirection == "leftwards":
            xdir = -1
        if self.ydirection == "downwards":
            ydir = -1
        self.vector = Point (xdir * random.random (), ydir * random.random ()) # unit vector

    def scale (self, n):
        # scale n (0..1) so that it is between -0.5 .. 0.5
        return n - 0.5

    def reflect (self, paddle_position):
        # paddle_position is -0.5 .. 0.5, with 0 begin dead-center
        # I'm not sure yet how I want this to affect the reflection, so I'll ignore it for now
        if self.xdirection == "leftwards":
            self.xdirection = "rightwards"
        else:
            self.xdirection = "leftwards"
        self.vector = Point (-1 * self.vector.x, -1 * self.vector.y)

def handler (eh,mev):
    self = eh.instance_data
    def send_ball_position (self, eh):
        zd.send (eh, "", f'\{"x":"{self.location.x\}","y":"{self.location.y}"\}', mev)
    port = mev.datum.port
    v = mev.datum.v
    try:
        if port == "⟳":
            self.reset ()
            send_ball_position ()
        elif port == "tick":
            send_ball_position ()
        elif port == "reflect":
            position_on_paddle = v
            self.reflect (v)
            send_ball_position ()
        else:
            zd.send (eh, "✗", "*** bad input to StepBall.py ***", mev)
            
    except (e):
        zd.send (eh, "✗", "*** error in StepBall.py ***", mev)
        


def instantiate (reg,owner,name, arg, template_data):
    name_with_id = zd.gensymbol ( "StepBall")
    self = Count ()
    return zd.make_leaf ( name_with_id, owner, self, arg, handler)

# define template
def install (reg):
    zd.register_component (reg, zd.mkTemplate ("StepBall", None, instantiate))


