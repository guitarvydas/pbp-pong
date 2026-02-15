#!/usr/bin/env node

const WebSocket = require('ws');
const crypto = require('crypto');

function query(queryType, timeout = 5000) {
  return new Promise((resolve, reject) => {
    const requestId = crypto.randomUUID();
    const ws = new WebSocket('ws://localhost:8082');
    
    const timer = setTimeout(() => {
      ws.close();
      reject(new Error('Query timeout'));
    }, timeout);
    
    ws.on('open', () => {
      ws.send(JSON.stringify({ id: requestId, query: queryType }));
    });
    
    ws.on('message', (data) => {
      try {
        const response = JSON.parse(data.toString());
        if (response.id === requestId) {
          clearTimeout(timer);
          ws.close();
          
          if (response.error) {
            reject(new Error(response.error));
          } else {
            resolve(response.result);
          }
        }
      } catch (e) {
        clearTimeout(timer);
        ws.close();
        reject(e);
      }
    });
    
    ws.on('error', (err) => {
      clearTimeout(timer);
      reject(err);
    });
  });
}

// CLI usage
if (require.main === module) {
  const queryType = process.argv[2] || 'canvas_size';
  
  query(queryType)
    .then(result => {
      console.log(JSON.stringify(result, null, 2));
      process.exit(0);
    })
    .catch(err => {
      console.error(`Error: ${err.message}`, { file: process.stderr });
      process.exit(1);
    });
}

module.exports = { query };
