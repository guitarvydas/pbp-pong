Perfect! Here's a clean test jig that supports both manual and programmatic command injection:

## Architecture

```
Manual CLI:      ./send-command (interactive)
Programmatic:    ./send-command '{"type":"ball","x":100}'
                        ↓
                  TCP Socket (port 8081)
                        ↓
                   Daemon (bridge)
                        ↓
                  WebSocket (port 8080)
                        ↓
                   Browser GUI
```

## Implementation

**1. Daemon (test-daemon.js)**

```javascript
#!/usr/bin/env node

const WebSocket = require('ws');
const net = require('net');

// WebSocket server for GUI
const wss = new WebSocket.Server({ port: 8080 });
let guiClient = null;

wss.on('connection', (ws) => {
  console.log('[Daemon] GUI connected');
  guiClient = ws;
  
  ws.on('close', () => {
    console.log('[Daemon] GUI disconnected');
    guiClient = null;
  });
});

// TCP server for command injection
const cmdServer = net.createServer((socket) => {
  console.log('[Daemon] Command client connected');
  
  socket.on('data', (data) => {
    const cmd = data.toString().trim();
    console.log('[Daemon] Received command:', cmd);
    
    if (guiClient && guiClient.readyState === WebSocket.OPEN) {
      guiClient.send(cmd);
      socket.write('OK\n');
    } else {
      socket.write('ERROR: No GUI connected\n');
    }
  });
  
  socket.on('end', () => {
    console.log('[Daemon] Command client disconnected');
  });
});

cmdServer.listen(8081, 'localhost', () => {
  console.log('[Daemon] Command server listening on localhost:8081');
  console.log('[Daemon] WebSocket server listening on localhost:8080');
  console.log('[Daemon] Ready for GUI connection and commands');
});
```

**2. CLI Tool (send-command.js)**

```javascript
#!/usr/bin/env node

const net = require('net');
const readline = require('readline');

function sendCommand(cmd, callback) {
  const client = net.connect(8081, 'localhost', () => {
    client.write(cmd + '\n');
  });
  
  client.on('data', (data) => {
    const response = data.toString().trim();
    if (callback) callback(response);
    client.end();
  });
  
  client.on('error', (err) => {
    console.error('Error connecting to daemon:', err.message);
    console.error('Make sure test-daemon.js is running');
    process.exit(1);
  });
}

// Programmatic mode: send single command from argument
if (process.argv.length > 2) {
  const cmd = process.argv.slice(2).join(' ');
  sendCommand(cmd, (response) => {
    console.log(response);
    process.exit(0);
  });
}
// Interactive mode: prompt for commands
else {
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
    prompt: 'CMD> '
  });
  
  console.log('Interactive command mode. Type JSON commands or Ctrl+C to exit.');
  rl.prompt();
  
  rl.on('line', (line) => {
    if (line.trim()) {
      sendCommand(line.trim(), (response) => {
        console.log('  →', response);
        rl.prompt();
      });
    } else {
      rl.prompt();
    }
  });
  
  rl.on('close', () => {
    console.log('\nExiting');
    process.exit(0);
  });
}
```

**3. GUI (client.html)**

```html
<!DOCTYPE html>
<html>
<head>
  <title>Test GUI</title>
  <style>
    body { 
      margin: 20px; 
      font-family: monospace;
      background: #1e1e1e;
      color: #d4d4d4;
    }
    #canvas { 
      border: 2px solid #4ec9b0; 
      background: #000;
      display: block;
      margin: 20px 0;
    }
    #log {
      background: #252526;
      padding: 10px;
      height: 200px;
      overflow-y: auto;
      border: 1px solid #3e3e42;
    }
    .log-entry {
      margin: 2px 0;
      font-size: 12px;
    }
  </style>
</head>
<body>
  <h2>Test GUI - Slave Display</h2>
  <canvas id="canvas" width="800" height="600"></canvas>
  <div id="log"></div>

  <script>
    const canvas = document.getElementById('canvas');
    const ctx = canvas.getContext('2d');
    const logDiv = document.getElementById('log');
    
    // Display state
    let objects = {};
    
    function log(msg) {
      const entry = document.createElement('div');
      entry.className = 'log-entry';
      entry.textContent = `[${new Date().toLocaleTimeString()}] ${msg}`;
      logDiv.appendChild(entry);
      logDiv.scrollTop = logDiv.scrollHeight;
    }
    
    function render() {
      // Clear canvas
      ctx.fillStyle = '#000';
      ctx.fillRect(0, 0, canvas.width, canvas.height);
      
      // Draw all objects
      for (const [id, obj] of Object.entries(objects)) {
        if (obj.type === 'ball') {
          ctx.fillStyle = '#ffffff';
          ctx.beginPath();
          ctx.arc(obj.x, obj.y, obj.radius || 10, 0, Math.PI * 2);
          ctx.fill();
        } else if (obj.type === 'paddle') {
          ctx.fillStyle = '#4ec9b0';
          ctx.fillRect(obj.x, obj.y, obj.width || 20, obj.height || 100);
        }
      }
    }
    
    // Connect to daemon
    const ws = new WebSocket('ws://localhost:8080');
    
    ws.onopen = () => {
      log('Connected to daemon');
    };
    
    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        log(`Received: ${JSON.stringify(data)}`);
        
        // Update object state
        const id = data.id || data.type;
        objects[id] = { ...objects[id], ...data };
        
        render();
      } catch (e) {
        log(`Error parsing message: ${e.message}`);
      }
    };
    
    ws.onclose = () => {
      log('Disconnected from daemon');
    };
    
    ws.onerror = (error) => {
      log(`WebSocket error: ${error.message}`);
    };
    
    // Initial render
    render();
  </script>
</body>
</html>
```

## Usage

**Setup:**

```bash
chmod +x test-daemon.js send-command.js
npm install ws  # if not already installed
```

**Run the daemon:**

```bash
./test-daemon.js
```

**Open GUI in browser:**

```
file:///path/to/client.html
```

or serve it and open `http://localhost:PORT/client.html`

**Manual commands (interactive):**

```bash
./send-command
CMD> {"type":"ball","x":400,"y":300}
  → OK
CMD> {"type":"paddle","id":"left","x":50,"y":250}
  → OK
CMD> {"type":"ball","x":500,"y":200,"radius":15}
  → OK
```

**Programmatic commands (one-shot):**

```bash
./send-command '{"type":"ball","x":400,"y":300}'
./send-command '{"type":"paddle","id":"left","x":50,"y":250}'
```

**From a script:**

```bash
#!/bin/bash
# animate.sh - Move ball across screen
for x in {0..800..10}; do
  ./send-command "{\"type\":\"ball\",\"x\":$x,\"y\":300}"
  sleep 0.05
done
```

This gives you complete flexibility - type commands by hand interactively or script them programmatically!