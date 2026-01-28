import asyncio
import websockets
import json
import uuid

async def test_client():
    uri = "ws://localhost:8000/ws/asp"
    print(f"Connecting to {uri}...")
    try:
        async with websockets.connect(uri) as websocket:
            print("Connected!")
            
            # Send CONNECT
            connect_msg = {
                "type": "CONNECT",
                "client_id": "debug-script",
                "version": "1.0"
            }
            await websocket.send(json.dumps(connect_msg))
            print(f"Sent: {connect_msg}")

            # Wait for messages
            while True:
                try:
                    message = await asyncio.wait_for(websocket.recv(), timeout=5.0)
                    data = json.loads(message)
                    print(f"Received: {data['type']}")
                    if data['type'] == 'STATE_UPDATE':
                        print(f"  > Content: {str(data)[:100]}...")
                except asyncio.TimeoutError:
                    print("No message received in 5s...")
                    # Send Ping
                    ping = {
                        "type": "INTENT",
                        "payload": {"name": "ping"},
                        "ref_id": str(uuid.uuid4())
                    }
                    await websocket.send(json.dumps(ping))
                    print(f"Sent Ping: {ping}")

    except Exception as e:
        print(f"Connection Failed: {e}")

if __name__ == "__main__":
    try:
        asyncio.run(test_client())
    except KeyboardInterrupt:
        print("\nStopped.")
