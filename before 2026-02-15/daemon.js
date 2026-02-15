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

// WebSocket server for GUI (port 8080)
const wss = new WebSocket.Server({ port: 8080 });
let guiClient = null;

// Track pending GUI queries: requestId -> query WebSocket client
const pendingGuiQueries = new Map();

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
      
      if (response.id && pendingGuiQueries.has(response.id)) {
        const queryClient = pendingGuiQueries.get(response.id);
        queryClient.send(JSON.stringify(response));
        pendingGuiQueries.delete(response.id);
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

// WebSocket server for queries (port 8082)
const queryWss = new WebSocket.Server({ port: 8082 });

queryWss.on('connection', (ws) => {
  console.log('[Daemon] Query client connected');
  
  ws.on('message', (data) => {
    try {
      const msg = JSON.parse(data.toString());
      const response = { id: msg.id };
      
      // Handle queries the daemon can answer directly
      switch (msg.query) {
        case 'canvas_size':
          response.result = DEFAULTS;
          ws.send(JSON.stringify(response));
          break;
        
        case 'defaults':
          response.result = DEFAULTS;
          ws.send(JSON.stringify(response));
          break;
        
        case 'objects':
          // Forward to GUI
          if (guiClient && guiClient.readyState === WebSocket.OPEN) {
            pendingGuiQueries.set(msg.id, ws);
            guiClient.send(JSON.stringify(msg));
          } else {
            response.error = 'No GUI connected';
            ws.send(JSON.stringify(response));
          }
          break;
        
        default:
          response.error = `Unknown query: ${msg.query}`;
          ws.send(JSON.stringify(response));
      }
    } catch (e) {
      console.error('[Daemon] Error handling query:', e.message);
    }
  });
  
  ws.on('close', () => {
    console.log('[Daemon] Query client disconnected');
  });
});

// TCP server for command injection (port 8081)
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
  console.log('[Daemon] WebSocket server (GUI) listening on localhost:8080');
  console.log('[Daemon] WebSocket server (queries) listening on localhost:8082');
  console.log('[Daemon] Ready for GUI connection, commands, and queries');
  console.log('[Daemon] DEFAULTS:', JSON.stringify(DEFAULTS, null, 2));
});
