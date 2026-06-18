import asyncio
import websockets

async def test():
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyMjQiLCJ1c2VybmFtZSI6InJlbmFuIiwiZXhwIjoxNzgxODI0OTE2fQ.jhDR6pFufuGKkxiOyBKgPzXMUkQJdZ61HQ1wfDS6kfg"
    async with websockets.connect(f"ws://127.0.0.1:8000/ws?token={token}") as ws:
        await ws.send("fala um filme ai")
        print(await ws.recv())
        


asyncio.run(test())

