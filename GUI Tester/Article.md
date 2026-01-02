# Building a Command-Line Test Jig for Browser-Based Game UIs

**Or: How to debug your client-server game without clicking around like a caveman**

## The Problem

You're building a game with a distributed MVC architecture—server handles all the logic, browser client is just a "dumb" display that renders what it's told. Classic setup for networked games.

But here's the annoying part: every time you want to test the client's rendering, you need to fire up the whole server, connect, trigger game events, and _hope_ you can reproduce the specific visual state you're trying to debug. Want to see how the ball looks at exactly x=237, y=412? Good luck clicking your way there.

What you really want is a **test jig**—a way to puppet the GUI from the command line, sending it arbitrary rendering commands on demand. Both manually (for interactive debugging) and programmatically (for automated visual tests).

## The Architecture

Here's what we built:

```
Manual CLI:      ./send-command (interactive REPL)
Programmatic:    ./send-command '{"x":100,"y":200}'
Animation:       ./bounce.sh (scripted sequences)
                        ↓
                  TCP Socket (port 8081)
                        ↓
              Daemon (message bridge)
                        ↓
                WebSocket (port 8080)
                        ↓
              Browser GUI (pure slave)
```

Three components, clean separation of concerns:

### 1. The Daemon (test-daemon.js)

A Node.js process that acts as a bridge between two worlds:

- **WebSocket server** (port 8080) for the browser GUI
- **TCP socket server** (port 8081) for command injection

The daemon is dead simple—it just forwards messages. When a command arrives on the TCP socket, it gets pushed through the WebSocket to the browser. That's it.

Key insight: **proper line buffering** on the TCP side. TCP is a stream protocol, so rapid commands can arrive concatenated. The daemon splits on newlines to ensure each command is a discrete message.

### 2. The CLI Tool (send-command.js)

A dual-mode tool that talks to the daemon over TCP:

**Interactive mode** (no arguments):

```bash
./send-command
CMD> {"type":"ball","x":400,"y":300}
  → OK
CMD> {"type":"paddle","id":"left","x":50,"y":250}
  → OK
```

**Programmatic mode** (with arguments):

```bash
./send-command '{"type":"ball","x":400,"y":300}'
```

This gives you both REPL-style debugging and scriptability. Same tool, different contexts.

### 3. The Browser GUI (client.html)

A pure slave display—no logic, just rendering. It:

- Connects to the daemon's WebSocket
- Maintains a dictionary of display objects
- Updates object state from incoming messages
- Renders everything on each update

Centralized defaults make it easy to tweak visual parameters:

```javascript
const DEFAULTS = {
  paddle: { width: 20, height: 100, color: '#4ec9b0' },
  ball: { radius: 10, color: '#ffffff' }
};
```

## Using It

**Setup:**

```bash
# Terminal 1: Start the daemon
./test-daemon.js

# Open client.html in browser
# (daemon logs "GUI connected")
```

**Manual debugging:**

```bash
./send-command
CMD> {"type":"ball","x":400,"y":300}
CMD> {"type":"paddle","id":"left","x":50,"y":250,"height":150}
```

Type JSON, see results instantly. No clicking, no complex reproduction steps.

**Scripted animation:**

```zsh
#!/bin/zsh
# bounce.sh - Animate a bouncing ball
for ((y=50; y<=550; y+=10)); do
  ./send-command "{\"type\":\"ball\",\"x\":400,\"y\":$y}"
  sleep 0.02
done

for ((y=540; y>=50; y-=10)); do
  ./send-command "{\"type\":\"ball\",\"x\":400,\"y\":$y}"
  sleep 0.02
done
```

Now you have reproducible visual tests. Run the script, watch the ball bounce, verify the rendering is smooth.

## Why This Works

**1. Clean separation of transport layers**

- TCP for command injection (easy to script with shell tools)
- WebSocket for browser communication (native browser API)
- Daemon bridges them without coupling

**2. Message-oriented, not request-response** The daemon doesn't wait for acknowledgments—it just pushes messages through. This makes animation smooth and prevents blocking.

**3. Stateless daemon** The daemon doesn't track game state—it's just a wire. This means:

- No synchronization bugs
- Trivial to reason about
- Easy to restart without losing anything

**4. Pure slave GUI** The browser has _zero_ game logic. It:

- Doesn't know about physics
- Doesn't interpolate between positions
- Just draws what it's told

This matches the final architecture where the game server will be authoritative anyway.

## What You Get

**For debugging:**

- Test edge cases instantly: `./send-command '{"type":"ball","x":-10,"y":300}'`
- Verify visual boundaries without complex game setup
- Reproduce exact visual states on demand

**For development:**

- Prototype rendering without implementing game logic
- Test performance with scripted animation sequences
- Verify client behavior in isolation

**For testing:**

- Automated visual regression tests
- Performance benchmarks (how many objects can we render at 60fps?)
- Screenshot comparisons at specific game states

## Lessons from the Trenches

**Bash version gotchas on macOS:** macOS ships with Bash 3.2 from 2007, which doesn't support three-argument brace expansion: `{0..800..10}` fails silently. Use zsh (the macOS default) or C-style for loops instead.

**TCP stream buffering matters:** Our first version concatenated rapid commands into malformed JSON. Line buffering with proper newline splitting fixed it.

**Defaults are configuration:** Putting magic numbers like paddle dimensions in a centralized `DEFAULTS` object makes the GUI self-documenting and easy to tune.

## The Bigger Picture

This pattern generalizes beyond games. Anytime you have:

- A browser-based UI that's driven by external data
- A need to test that UI in isolation
- A desire for scriptable, reproducible test scenarios

...this architecture works.

Replace "game objects" with "chart data" or "dashboard metrics" or "notification states"—same pattern, same benefits.

## Code

Want to build your own? The complete implementation is under 200 lines of JavaScript:

- Daemon: ~50 lines
- CLI tool: ~60 lines
- GUI: ~80 lines

Three files, zero dependencies beyond Node.js and the `ws` WebSocket library.

---

_This test jig emerged from building a distributed Pong implementation where server authority and client-server boundaries were paramount. Sometimes the best debugging tools are the ones you build yourself._