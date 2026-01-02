#!/bin/zsh
# bounce.sh - Bounce ball vertically

# Down
for ((y=50; y<=550; y+=10)); do
  ./send-command "{\"type\":\"ball\",\"x\":$y,\"y\":$y}"
  #sleep 0.02
done

# Up
for ((y=540; y>=50; y-=10)); do
  ./send-command "{\"type\":\"ball\",\"x\":$y,\"y\":$y}"
  #sleep 0.02
done
