# main.py
from fastapi import FastAPI, WebSocket
import httpx  # HTTP client for making requests
import asyncio

app = FastAPI()

async def fetch_bitcoin_data():
    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd")
        bitcoin_data = response.json()
        return bitcoin_data["bitcoin"]["usd"]

# WebSocket route for streaming data
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        bitcoin_price = await fetch_bitcoin_data()
        await websocket.send_text(f"Bitcoin Price (USD): {bitcoin_price}")
        await asyncio.sleep(10)  # Adjust the sleep duration as needed
