import asyncio
import websockets

async def test():
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyMjQiLCJ1c2VybmFtZSI6InJlbmFuIiwiZXhwIjoxNzgyMjU3MTc0fQ.0R9WPX50QPBrSraVx390BOuf7M6iX0AKMC7AXxuRiBA"
    async with websockets.connect(f"ws://127.0.0.1:8000/ws?token={token}") as ws:
        await ws.send("me ajuda ai")
        print(await ws.recv())
        


asyncio.run(test())

