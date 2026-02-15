#!/usr/bin/env python3

import asyncio
import websockets
import json
import sys
import uuid

async def query(query_type, host='localhost', port=8082, timeout=5.0):
    """
    Send a query to the daemon and wait for response.
    
    Args:
        query_type: Type of query ('canvas_size', 'defaults', 'objects')
        host: Daemon hostname
        port: Daemon WebSocket port
        timeout: Timeout in seconds
    
    Returns:
        Query result as Python dict/object
    """
    request_id = str(uuid.uuid4())
    query_msg = json.dumps({"id": request_id, "query": query_type})
    
    uri = f"ws://{host}:{port}"
    
    try:
        async with websockets.connect(uri) as websocket:
            await websocket.send(query_msg)
            
            response = await asyncio.wait_for(websocket.recv(), timeout=timeout)
            data = json.loads(response)
            
            if data.get('id') == request_id:
                if 'error' in data:
                    raise Exception(data['error'])
                return data.get('result')
            else:
                raise Exception('Response ID mismatch')
                
    except asyncio.TimeoutError:
        raise Exception('Query timeout')

# CLI usage
if __name__ == '__main__':
    query_type = sys.argv[1] if len(sys.argv) > 1 else 'canvas_size'
    
    try:
        result = asyncio.run(query(query_type))
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f'Error: {e}', file=sys.stderr)
        sys.exit(1)
