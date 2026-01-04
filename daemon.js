#!/usr/bin/env node

const WebSocket = require('ws');
const net = require('net');

// WebSocket server for GUI
const wss = new WebSocket.Server({ port: 8080 });
let guiClient = null;

// Track pending requests: requestId -> TCP socket
const pendingRequests = new Map();

wss.on('connection', (ws) => {
  console.log('[Daemon] GUI connected');
  guiClient = ws;
  
  ws.on('message', (data) => {
    // Handle responses from GUI
    try {
      const response = JSON.parse(data.toString());
      // console.log('[Daemon] Received response from GUI:', response);
      
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
      
      // console.log('[Daemon] Received command:', cmd);
      
      if (guiClient && guiClient.readyState === WebSocket.OPEN) {
        try {
          const parsed = JSON.parse(cmd);
          
          // If this has an ID (query or tracked command), register for response
          if (parsed.id) {
            pendingRequests.set(parsed.id, socket);
          }
          
          guiClient.send(cmd);
          
          // Only send OK for commands without ID (fire-and-forget)
          if (!parsed.id) {
            socket.write('OK\n');
          }
        } catch (e) {
          socket.write(`ERROR: Invalid JSON - ${e.message}\n`);
        }
      } else {
        socket.write('ERROR: No GUI connected\n');
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
});
