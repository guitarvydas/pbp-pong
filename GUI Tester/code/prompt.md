This bash script
```
#!/bin/bash
# animate.sh - Move ball across screen
for x in {0..800..10}; do
  cmd='{"type":"ball","x":' $x ',"y":300}'
  echo $cmd
  ./send-command $cmd
  sleep 0.05
done
```

gives me this error

./t4: line 4: {0..800..10}: command not found
