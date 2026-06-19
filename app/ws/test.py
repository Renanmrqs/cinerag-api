import asyncio
import websockets

async def test():
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyMjQiLCJ1c2VybmFtZSI6InJlbmFuIiwiZXhwIjoxNzgxODk2MTAwfQ.r8cxmTZ4R7GsqZ9KKLgsbbzVyy9zPXWRLQjQXAP78yw"
    async with websockets.connect(f"ws://127.0.0.1:8000/ws?token={token}") as ws:
        await ws.send("fala comigo bebe")
        print(await ws.recv())
        


asyncio.run(test())

