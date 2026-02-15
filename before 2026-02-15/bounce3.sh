#!/bin/zsh

echo '[' >/tmp/xx
echo '{"type":"ball","x":400,"y":300,"color":"#ff8800"},' >>/tmp/xx

for ((y=50; y<=550; y+=100)); do
  echo "{\"type\":\"ball\",\"x\":$y,\"y\":$y}," >>/tmp/xx
done

for ((y=548; y>=50; y-=100)); do
  echo "{\"type\":\"ball\",\"x\":$y,\"y\":$y}," >>/tmp/xx
done

echo '{"type":"ball","x":400,"y":300,"color":"#888800"}' >>/tmp/xx
echo ']' >>/tmp/xx
cat /tmp/xx

