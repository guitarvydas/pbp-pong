#!/usr/bin/env node

const net = require('net');

const client = net.connect(8081, 'localhost', () => {
  let buffer = '';
  
  process.stdin.on('data', (chunk) => {
    buffer += chunk.toString();
    
    // Process complete lines
    let lines = buffer.split('\n');
    buffer = lines.pop(); // Keep incomplete line in buffer
    
    for (const line of lines) {
      const cmd = line.trim();
      if (cmd) {
        client.write(cmd + '\n');
      }
    }
  });
  
  process.stdin.on('end', () => {
    // Send any remaining buffered data
    if (buffer.trim()) {
      client.write(buffer.trim() + '\n');
    }
    client.end();
  });
});

client.on('error', (err) => {
  console.error('Error connecting to daemon:', err.message);
  console.error('Make sure test-daemon.js is running');
  process.exit(1);
});

client.on('end', () => {
  process.exit(0);
});
