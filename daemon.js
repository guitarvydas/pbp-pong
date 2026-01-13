#!/usr/bin/env node

const WebSocket = require('ws');
const net = require('net');

// DEFAULTS - Single source of truth
const DEFAULTS = {
  canvas: {
    width: 800,
    height: 600
  },
  paddle: { 
    width: 20, 
    height: 100,
    color: '#4ec9b0'
  },
  ball: { 
    radius: 10,
    color: '#ffffff'
  }
};

// WebSocket server for GUI
const wss = new WebSocket.Server({ port: 8080 });
let guiClient = null;

// Track pending requests: requestId -> TCP socket
const pendingRequests = new Map();

wss.on('connection', (ws) => {
  console.log('[Daemon] GUI connected');
  guiClient = ws;
  
  // Send DEFAULTS to GUI on connection
  ws.send(JSON.stringify({ 
    type: 'init',
    defaults: DEFAULTS 
  }));
  
  ws.on('message', (data) => {
    // Handle responses from GUI
    try {
      const response = JSON.parse(data.toString());
      
      if (response.id && pendingRequests.has(response.id)) {
        const socket = pendingRequests.get(response.id);
        socket.write(JSON.stringify(response) + '\n');
        pendingRequests.delete(response.id);
      }
    } catch (e) {
      console.error('[Daemon] Error handling GUI response:', e.message);
    }
  });
  
  ws.on('close', () => {
    console.log('[Daemon] GUI disconnected');
    guiClient = null;
  });
});

// Handle queries that the daemon can answer directly
function handleDaemonQuery(msg, socket) {
  const response = { id: msg.id };
  
  switch (msg.query) {
    case 'canvas_size':
      response.result = DEFAULTS.canvas;
      break;
    
    case 'defaults':
      response.result = DEFAULTS;
      break;
    
    default:
      return false; // Not a daemon query, should forward to GUI
  }
  
  socket.write(JSON.stringify(response) + '\n');
  return true; // Handled
}

// TCP server for command injection
const cmdServer = net.createServer((socket) => {
  console.log('[Daemon] Command client connected');
  
  let buffer = '';
  
  socket.on('data', (data) => {
    buffer += data.toString();
    
    // Process complete lines (commands end with \n)
    let lines = buffer.split('\n');
    buffer = lines.pop(); // Keep incomplete line in buffer
    
    for (const line of lines) {
      const cmd = line.trim();
      if (!cmd) continue;
      
      try {
        const parsed = JSON.parse(cmd);
        
        // Check if this is a query the daemon can handle
        if (parsed.query && handleDaemonQuery(parsed, socket)) {
          continue; // Daemon handled it
        }
        
        // Otherwise, forward to GUI
        if (guiClient && guiClient.readyState === WebSocket.OPEN) {
          // If this has an ID (query for GUI), register for response
          if (parsed.id) {
            pendingRequests.set(parsed.id, socket);
          }
          
          guiClient.send(cmd);
          
          // Only send OK for commands without ID (fire-and-forget)
          if (!parsed.id) {
            socket.write('OK\n');
          }
        } else {
          socket.write('ERROR: No GUI connected\n');
        }
      } catch (e) {
        socket.write(`ERROR: Invalid JSON - ${e.message}\n`);
      }
    }
  });
  
  socket.on('end', () => {
    console.log('[Daemon] Command client disconnected');
    // Clean up any pending requests from this socket
    for (const [id, sock] of pendingRequests.entries()) {
      if (sock === socket) {
        pendingRequests.delete(id);
      }
    }
  });
});

cmdServer.listen(8081, 'localhost', () => {
  console.log('[Daemon] Command server listening on localhost:8081');
  console.log('[Daemon] WebSocket server listening on localhost:8080');
  console.log('[Daemon] Ready for GUI connection and commands');
  console.log('[Daemon] DEFAULTS:', JSON.stringify(DEFAULTS, null, 2));
});
