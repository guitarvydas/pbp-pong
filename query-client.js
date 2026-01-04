#!/usr/bin/env node

const net = require('net');
const crypto = require('crypto');

function query(queryType, timeout = 5000) {
  return new Promise((resolve, reject) => {
    const requestId = crypto.randomUUID();
    const queryMsg = JSON.stringify({ id: requestId, query: queryType });
    
    const client = net.connect(8081, 'localhost', () => {
      client.write(queryMsg + '\n');
    });
    
    let buffer = '';
    const timer = setTimeout(() => {
      client.end();
      reject(new Error('Query timeout'));
    }, timeout);
    
    client.on('data', (data) => {
      buffer += data.toString();
      
      // Try to parse response
      try {
        const response = JSON.parse(buffer);
        if (response.id === requestId) {
          clearTimeout(timer);
          client.end();
          
          if (response.error) {
            reject(new Error(response.error));
          } else {
            resolve(response.result);
          }
        }
      } catch (e) {
        // Incomplete JSON, wait for more data
      }
    });
    
    client.on('error', (err) => {
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
      console.error('Query failed:', err.message);
      process.exit(1);
    });
}

module.exports = { query };
