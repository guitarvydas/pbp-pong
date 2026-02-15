#!/bin/zsh
# animate.sh - Move ball across screen
for x in {0..800..10}; do
  ./send-command "{\"type\":\"ball\",\"x\":$x,\"y\":300}"
  #sleep 0.05
done
