Key changes:

DEFAULTS object at the top with all default dimensions and colors
Explicit undefined checks (obj.width !== undefined) instead of || to allow zero values
Color defaults added for both objects

Now you can easily adjust all defaults in one place, and commands can still override any property:

# Uses all defaults (20x100, teal)
./send-command '{"type":"paddle","id":"left","x":50,"y":250}'

# Override just width
./send-command '{"type":"paddle","id":"right","x":730,"y":250,"width":15}'

# Custom color
./send-command '{"type":"ball","x":400,"y":300,"color":"#ff0000"}'
