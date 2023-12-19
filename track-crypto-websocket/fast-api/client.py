# client.py
import asyncio
import websockets

async def receive_data():
    uri = "ws://localhost:8000/ws"  # Replace with your FastAPI server URI
    async with websockets.connect(uri) as websocket:
        while True:
            data = await websocket.recv()
            print(f"Received: {data}")

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(receive_data())
