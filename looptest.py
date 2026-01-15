import json
import sys
sys.path.insert(0, './pbp/kernel')
import kernel0d as zd

class WH:
    def __init__(self):
        self.previous_x = 0
        self.width = None
        self.height = None
        self.state = "idle"

def handler (eh,mev):
    try:
        self = eh.instance_data
        if mev.port == 'width':
            self.width = int (mev.datum.v) ## just save the value
        elif mev.port == '':
            x = int (mev.datum.v)

### begin generated                
            def enter_idle (): self.state = "idle"
            def action_idle ():
                if x < 0:
                    exit_idle ()
                    enter_wait_for_zero_recrossing ()
                elif x > self.width:
                    exit_idle ()
                    enter_wait_for_w_recrossing ()
                else:
                    zd.send (eh, "", mev.datum.v, mev) ## send a trigger to keep running the loop
            def exit_idle (): pass

            def enter_wait_for_zero_recrossing ():
                zd.send (eh, "rev", "", mev)
                self.state = "wait for zero re-crossing"
            def action_wait_for_zero_recrossing ():
                if x >= 0:
                    exit_wait_for_zero_recrossing ()
                    enter_idle ()
                    zd.send (eh, "", mev.datum.v, mev) ## send a trigger to keep running the loop
            def exit_wait_for_zero_recrossing (): pass

            def enter_wait_for_w_recrossing ():
                zd.send (eh, "rev", "", mev)
                self.state = "wait for w re-crossing"
            def action_wait_for_w_recrossing ():
                if x <= self.width:
                    exit_wait_for_w_recrossing ()
                    enter_idle ()
                    zd.send (eh, "", mev.datum.v, mev) ## send a trigger to keep running the loop
            def exit_wait_for_w_recrossing (): pass

            if self.state == "idle":
                action_idle ()
            elif self.state == "wait for zero re-crossing":
                action_wait_for_zero_recrossing ()
            elif self.state == "wait for w re-crossing":
                action_wait_for_zero_recrossing ()
### end generated                

        else:
            raise ValueError(f"unrecognized port {mev.port}")
    except (e):
        zd.send (eh, "✗", f"*** error in looptest.py *** {e}", mev)

        
def instantiate (reg,owner,name, arg, template_data):
    name_with_id = zd.gensymbol ( "Loop Test")
    self = WH ()
    return zd.make_leaf ( name_with_id, owner, self, arg, handler)

# define template
def install (reg):
    zd.register_component (reg, zd.mkTemplate ("Loop Test", None, instantiate))


