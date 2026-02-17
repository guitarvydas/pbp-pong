#!/usr/bin/env node
// send-glsl.js — send a file's contents to the relay server
//
// Usage: node send-glsl.js <filename|-&gt; [ws://host:port]
//   Use '-' as filename to read from stdin.
//   default server: ws://localhost:8765

const fs = require('fs');
const { WebSocket } = require('ws');

const file = process.argv[2] || null;
const server = process.argv[3] || 'ws://localhost:8765';

function sendToWs(src) {
  const ws = new WebSocket(`${server}?role=sender`);

  ws.on('open', () => {
    ws.send(src);
    console.log(`sent ${src.length} bytes`);
    ws.close();
  });

  ws.on('error', (err) => {
    console.error(`websocket error: ${err.message}`);
    process.exit(1);
  });
}

if (file && file !== '-') {
  sendToWs(fs.readFileSync(file, 'utf-8'));
} else {
  // Read all of stdin, then send
  let buf = '';
  process.stdin.setEncoding('utf-8');
  process.stdin.on('data', (chunk) => { buf += chunk; });
  process.stdin.on('end', () => { sendToWs(buf); });
}
