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
