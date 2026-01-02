#!/bin/zsh
# bounce.sh - Smooth bouncing ball (no sleep needed)

for ((y=50; y<=550; y+=10)); do
  ./send-command "{\"type\":\"ball\",\"x\":$y,\"y\":$y}"
done

for ((y=548; y>=50; y-=10)); do
  ./send-command "{\"type\":\"ball\",\"x\":$y,\"y\":$y}"
done
