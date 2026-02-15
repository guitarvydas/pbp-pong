#!/usr/bin/env node

const net = require('net');

let buffer = '';

// Collect all stdin first
process.stdin.on('data', (chunk) => {
  buffer += chunk.toString();
});

process.stdin.on('end', () => {
  // Connect and send after we have all the data
  const client = net.connect(8081, 'localhost', () => {
    const lines = buffer.split('\n');
    
    for (const line of lines) {
      const cmd = line.trim();
      if (cmd) {
        client.write(cmd + '\n');
      }
    }
    
    client.end();
  });

  client.on('error', (err) => {
    console.error('Error connecting to daemon:', err.message);
    console.error('Make sure test-daemon.js is running');
    process.exit(1);
  });

  client.on('end', () => {
    process.exit(0);
  });
});
