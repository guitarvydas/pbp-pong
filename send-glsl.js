#!/usr/bin/env node
// send-glsl.js — send a file's contents to the relay server
//
// Usage: node send-glsl.js <filename> [ws://host:port]
//   default server: ws://localhost:8765

const fs = require('fs');
const { WebSocket } = require('ws');

const file = process.argv[2];
if (!file) {
  console.error('usage: node send-glsl.js <filename> [ws://host:port]');
  process.exit(1);
}

const server = process.argv[3] || 'ws://localhost:8765';
const src = fs.readFileSync(file, 'utf-8');

const ws = new WebSocket(`${server}?role=sender`);

ws.on('open', () => {
  ws.send(src);
  console.log(`sent ${src.length} bytes from ${file}`);
  ws.close();
});

ws.on('error', (err) => {
  console.error(`websocket error: ${err.message}`);
  process.exit(1);
});
