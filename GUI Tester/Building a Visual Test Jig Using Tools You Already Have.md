# Building a Visual Test Jig Using Tools You Already Have

## The Components Are Already Here

When building interactive systems with visual output, we face a common problem: how do we test our logic and see the results without building elaborate testing frameworks?

Consider what we already have at our disposal:

**A textual REPL**: The command line. We can type commands manually for interactive exploration, or write scripts and programs that generate commands for automated testing.

**A visual output device**: The web browser. It renders graphics, handles real-time updates via WebSocket, and runs on every development machine.

**A transport format**: JSON. Human-readable, machine-parseable, universally supported. No custom binary protocols needed.

The architecture emerges naturally from these existing tools.

## Design Principle: Separation of Concerns

The key insight is to treat the REPL and GUI as **separate, isolated components** connected by a message protocol:

```
Command Generator  →  [JSON messages]  →  Visual Renderer
   (REPL side)                              (GUI side)
```

The GUI acts as a **pure slave**—it waits for commands and renders what it's told. It receives JSON like:

```json
{"type": "ball", "x": 400, "y": 300}
{"type": "paddle", "id": "left", "x": 50, "y": 250}
```

And simply draws the corresponding objects. No computation, no state transitions, no logic. Just rendering.

The REPL side **generates commands**. These might come from:

- Manual typing for interactive debugging
- Shell scripts for animation sequences
- Programs implementing physics or game logic
- Test harnesses validating behavior

## Implementation Architecture

Three lightweight components provide the complete system:

### 1. The Daemon (Message Bridge)

A Node.js process that bridges two transport layers:

- TCP socket server (port 8081) for command injection
- WebSocket server (port 8080) for browser connection

```javascript
// Simplified structure
const cmdServer = net.createServer((socket) => {
  socket.on('data', (data) => {
    // Parse incoming TCP stream
    // Forward complete JSON commands to WebSocket
    if (guiClient) {
      guiClient.send(command);
    }
  });
});
```

The daemon is **stateless**—it doesn't track game objects or maintain history. It simply forwards messages, making it trivial to reason about and debug.

### 2. The CLI Tool (Command Generator)

A dual-mode tool that connects to the daemon:

**Interactive mode**:

```bash
./send-command
CMD> {"type":"ball","x":400,"y":300}
  → OK
CMD> {"type":"paddle","id":"left","x":50,"y":250}
  → OK
```

**Programmatic mode**:

```bash
./send-command '{"type":"ball","x":400,"y":300}'
```

This flexibility enables both exploratory testing (type commands by hand) and scripted testing (generate commands programmatically).

### 3. The Browser GUI (Pure Renderer)

An HTML5 Canvas application that:

- Connects to the daemon via WebSocket
- Maintains a dictionary of display objects
- Updates state from incoming JSON messages
- Renders on each update

```javascript
ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  
  // Update object state
  objects[data.id] = { ...objects[data.id], ...data };
  
  // Render (throttled to 60fps)
  requestAnimationFrame(render);
};
```

The renderer has **zero game logic**. It doesn't know about physics, collision detection, or scoring. It only knows how to draw what the JSON describes.

## Usage Patterns

### Interactive Debugging

Type commands manually to explore visual states:

```bash
./send-command
CMD> {"type":"ball","x":400,"y":300}
CMD> {"type":"ball","x":-10,"y":300}  # Test edge case
CMD> {"type":"paddle","height":200}    # Test large paddle
```

See results immediately. No need to trigger specific game conditions or click through UI to reach the state you want to test.

### Scripted Animation

Generate command sequences programmatically:

```bash
#!/bin/zsh
# Animate ball moving across screen
for ((x=0; x<=800; x+=5)); do
  ./send-command "{\"type\":\"ball\",\"x\":$x,\"y\":300}"
done
```

Watch the visual output to verify rendering performance, smoothness, and correctness.

### Physics Simulation

Write a command-line program that implements your game logic and sends position updates:

```javascript
// physics-sim.js
const dt = 1/60;
let ball = { x: 400, y: 300, vx: 5, vy: 3 };

setInterval(() => {
  // Update physics
  ball.x += ball.vx;
  ball.y += ball.vy;
  
  // Bounce at edges
  if (ball.x < 0 || ball.x > 800) ball.vx *= -1;
  if (ball.y < 0 || ball.y > 600) ball.vy *= -1;
  
  // Send to GUI
  sendCommand({ type: 'ball', x: ball.x, y: ball.y });
}, dt * 1000);
```

Now you can **watch your physics work** in real-time. If something looks wrong visually, you know the problem is in your simulation code, not the renderer.

## Advantages of This Approach

**Visual feedback without numeric decoding**: Instead of reading console output like `Ball position: (237.4, 412.8)`, you see the ball at that position. Spatial bugs become immediately obvious.

**Test logic in isolation**: Your physics simulation or game AI can run on the command line, completely separate from rendering. This isolation enables:

- Unit testing of logic without browser overhead
- Running simulations faster than real-time
- Recording and replaying command sequences

**Experiment freely**: Want to see what a paddle three times normal size looks like? Send the command. Want to test ball behavior at x=-50? Send the command. No need to modify code, recompile, or trigger complex game states.

**Architectural clarity from day one**: The strict separation between command generator (logic) and renderer (display) matches the distributed MVC architecture you'll need for networked multiplayer anyway. Your test jig **is** your client-server prototype.

## Extensions and Variations

The basic architecture supports natural extensions:

**Sophisticated command generators**: Build a GUI controller with sliders that generate JSON commands in real-time. Drag a slider labeled "ball.x" and watch the ball move as JSON commands flow to the renderer.

**Record and replay**: Log all commands to a file, then replay them later to reproduce exact visual sequences. Essential for debugging intermittent rendering issues.

**Multiple renderers**: Point different browsers at the daemon. They all receive the same commands and should render identically. Great for cross-browser testing.

**Alternative command sources**: Replace shell scripts with Python, Ruby, or any language that can send TCP packets. The protocol (JSON over TCP) remains constant.

## Performance Considerations

Two optimizations enable smooth animation:

**1. Render throttling** using `requestAnimationFrame`:

```javascript
let renderScheduled = false;

ws.onmessage = (event) => {
  updateState(JSON.parse(event.data));
  
  if (!renderScheduled) {
    renderScheduled = true;
    requestAnimationFrame(() => {
      render();
      renderScheduled = false;
    });
  }
};
```

This ensures rendering never exceeds 60fps, regardless of command rate.

**2. Minimal logging**: Comment out console output in hot paths. DOM manipulation for logging is expensive when commands arrive rapidly.

## Conclusion

The architecture requires no frameworks, no build systems, no configuration. Three simple components totaling under 200 lines:

- Daemon: Forwards messages between TCP and WebSocket
- CLI tool: Sends JSON commands over TCP
- Browser GUI: Renders based on JSON commands

Each component has a single, clear responsibility. The protocol (JSON) is self-documenting and human-readable. The separation of concerns makes each part independently testable.

Most importantly: **you built this with tools that already exist**. The command line is your REPL. JSON is your protocol. The browser is your display. A tiny daemon connects them.

Sometimes the best architecture is the one that uses what's already there.