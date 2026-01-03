#!/bin/zsh

echo '{"type":"ball","x":400,"y":300,"color":"#ff0000"}'

for ((y=50; y<=550; y+=10)); do
  echo "{\"type\":\"ball\",\"x\":$y,\"y\":$y}"
done

for ((y=548; y>=50; y-=10)); do
  echo "{\"type\":\"ball\",\"x\":$y,\"y\":$y}"
done
