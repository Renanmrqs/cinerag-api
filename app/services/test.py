import asyncio
import websockets

async def test():
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJtYXJsb3MiLCJleHAiOjE3ODA3ODEyNjR9.lLuEMppRI_9PZFKV3wXKbFDHbt4g5Pk6kD0mTAsFatU"
    async with websockets.connect(f"ws://127.0.0.1:8000/ws?token={token}") as ws:
        await ws.send("ja vi, puxa outro ai")
        print(await ws.recv())
        


asyncio.run(test())