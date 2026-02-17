#!/usr/bin/env node
// relay.js — WebSocket relay server
// Browser connects and waits. CLI tool connects, sends GLSL, relay forwards it.
//
// Usage: node relay.js [port]
//   default port: 8765

const { WebSocketServer } = require('ws');

const PORT = parseInt(process.argv[2] || '8765', 10);
const wss = new WebSocketServer({ port: PORT });

let viewer = null;

wss.on('connection', (ws, req) => {
  const url = new URL(req.url, `http://localhost:${PORT}`);
  const role = url.searchParams.get('role');

  if (role === 'viewer') {
    viewer = ws;
    console.log('viewer connected');
    ws.on('close', () => { viewer = null; console.log('viewer disconnected'); });

  } else {
    // sender — accumulate entire message then relay
    console.log('sender connected');
    ws.on('message', (data) => {
      const text = data.toString();
      if (viewer && viewer.readyState === 1) {
        viewer.send(text);
        console.log(`relayed ${text.length} bytes to viewer`);
      } else {
        console.error('no viewer connected — message dropped');
      }
    });
    ws.on('close', () => { console.log('sender disconnected'); });
  }
});

console.log(`relay listening on ws://localhost:${PORT}`);
