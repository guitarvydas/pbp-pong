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
  
  let buffer = '';
  
  socket.on('data', (data) => {
    buffer += data.toString();
    
    // Process complete lines (commands end with \n)
    let lines = buffer.split('\n');
    buffer = lines.pop(); // Keep incomplete line in buffer
    
    for (const line of lines) {
      const cmd = line.trim();
      if (!cmd) continue;
      
      console.log('[Daemon] Received command:', cmd);
      
      if (guiClient && guiClient.readyState === WebSocket.OPEN) {
        guiClient.send(cmd);
        socket.write('OK\n');
      } else {
        socket.write('ERROR: No GUI connected\n');
      }
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
