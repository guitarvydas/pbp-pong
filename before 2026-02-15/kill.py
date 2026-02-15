import sys
import time
sys.path.insert(0, './pbp/kernel')
import kernel0d as zd

from dataclasses import dataclass
from typing import Optional

@dataclass
class State:
    kill: bool = False

def handler (eh,mev):
    self = eh.instance_data
    if mev.port == "":
        self.kill = True
        zd.forward (eh, "", mev)
    elif not self.kill and mev.port == "in":
        zd.forward (eh, "out", mev)
        
def instantiate (reg,owner,name, arg, template_data):
    name_with_id = zd.gensymbol ( "kill")
    self = State ()
    return zd.make_leaf ( name_with_id, owner, self, arg, handler)

# define template
def install (reg):
    zd.register_component (reg, zd.mkTemplate ("kill", None, instantiate))


