import sys
import os
import time
sys.path.insert(0, './pbp/kernel')
import kernel0d as zd

class WH:
    def __init__(self):
        self.x = 0
        self.y = 350
        self.width = None
        self.height = None
        self.state = 'idle'
        self.dir = 1

def handler (eh,mev):
    self = eh.instance_data
    print (f'test gets [{mev.port}:{mev.datum.v}]', file=sys.stderr)
    try:
        if 'width' == mev.port:
            self.width = int (mev.datum.v)
        elif 'height' == mev.port:
            self.height = int (mev.datum.v)
        elif 'rev' == mev.port:
            self.dir = -1 * self.dir
            self.x = self.x + (self.dir * int (self.width / 20))
            zd.send (eh, "", "{" + f'"type":"ball","x":"{self.x}","y":{self.y},"color":"#ff0000"' + "}" , mev)
            zd.send (eh, "x", f'{self.x}' , mev)
        elif '' == mev.port:
            if self.state == 'idle':
                # send paddle image if first time
                zd.send (eh, "", '{' + f'"type":"paddle","id":"left","x":{self.x},"y":{self.y}' + '}', mev)
                zd.send (eh, "x", f'{self.x}' , mev)
                self.state = 'looping'
            self.x = self.x + (self.dir * int (self.width / 20))
            zd.send (eh, "", "{" + f'"type":"ball","x":"{self.x}","y":{self.y},"color":"#ff0000"' + "}" , mev)
            zd.send (eh, "x", f'{self.x}' , mev)
        else:
             zd.send (eh, "✗", f"unrecognized port '{mev.port}' in test.py", mev)
    except (err):
        zd.send (eh, "✗", f"*** error in test.py *** {err}", mev)
        
def instantiate (reg,owner,name, arg, template_data):
    name_with_id = zd.gensymbol ( "Test")
    self = WH ()
    return zd.make_leaf ( name_with_id, owner, self, arg, handler)

# define template
def install (reg):
    zd.register_component (reg, zd.mkTemplate ("Test", None, instantiate))


