# You Already Have the Tools for Building a Test Jig

## The Realization

We already have a built-in textual REPL—**it's the command line**. We can type commands manually, or write scripts and programs that generate commands. No framework needed, no custom tooling required.

We already have a standard GUI—**the browser**. It renders graphics, handles events, connects over WebSockets. It's on every machine.

The insight is simple: **treat the REPL and GUI as separate, isolated parts**.

## The Architecture

The GUI is just a **slave**, waiting for commands and rendering them. It doesn't think, doesn't compute, doesn't decide. It receives JSON like `{"type":"ball","x":400,"y":300}` and draws a ball. That's it.

The REPL **sends commands** to the GUI. You can type them interactively:

```bash
./send-command
CMD> {"type":"ball","x":400,"y":300}
CMD> {"type":"paddle","id":"left","x":50,"y":250}
```

Or generate them programmatically:

```zsh
for ((x=0; x<=800; x+=5)); do
  ./send-command "{\"type\":\"ball\",\"x\":$x,\"y\":300}"
done
```

A lightweight **daemon** bridges the two—it accepts commands over TCP and forwards them to the browser over WebSocket. No state, no logic, just message passing.

## Why This Matters

**Visual experimentation without deciphering number streams.** Instead of staring at console output like:

```
Ball position: (237.4, 412.8)
Ball velocity: (3.2, -1.5)
Paddle position: (50, 267)
```

You send commands and **see** the result. Test edge cases instantly: What happens when the ball is at x=-10? Send the command, watch it render.

**The command line is your test harness.** Write a script that simulates physics, sends position updates, and watch the ball bounce in real-time. Debug rendering without implementing game logic. Verify client behavior in isolation.

**Separation enables iteration.** The GUI doesn't care if commands come from a shell script, a Node.js physics engine, or a Python simulator. The command generator doesn't care if the GUI is HTML5 Canvas, WebGL, or a native window. They're decoupled.

## Beyond Simple Commands

You could build a **more sophisticated REPL**. Imagine a floating slider widget that generates JSON commands as you drag, sending them directly to the GUI. Or a timeline scrubber that replays recorded game sequences frame-by-frame.

You can **test physics by creating a command-line program** that simulates ball motion, collision detection, or paddle AI—and watch it happen live in the browser. If something looks wrong visually, you know the problem is in your physics code, not the renderer.

The architecture scales from "type a command and see what happens" to "run complex simulations and validate behavior."

## The Components

Three pieces, under 200 lines total:

**Daemon** (50 lines): Bridge between TCP socket (for commands) and WebSocket (for browser). No state, just forwarding.

**CLI Tool** (60 lines): Connects to daemon, sends JSON commands. Works interactively or programmatically.

**Browser GUI** (80 lines): WebSocket client that maintains display state and renders on command. Pure slave, zero logic.

No frameworks, no build steps, no configuration files.

## What You Get

- **Interactive debugging**: Send arbitrary commands, see immediate visual feedback
- **Scriptable testing**: Animate sequences, test edge cases, automate visual verification
- **Architectural clarity**: Clean separation between display and logic from day one
- **Future-proof**: Drop in different renderers, different command generators—the protocol stays the same

## The Insight

Sometimes the best tool is the one you already have. The command line is a REPL. The browser is a GUI. A tiny daemon connects them. Everything else is just sending messages.

That's the whole architecture.