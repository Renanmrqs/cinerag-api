import asyncio
import websockets

async def test():
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyMjQiLCJ1c2VybmFtZSI6InJlbmFuIiwiZXhwIjoxNzgyMjU5NjA0fQ.wMjiia20SKBTn3OIZgZ8W90VbKEugcmw8puldKFUiK4"
    async with websockets.connect(f"ws://127.0.0.1:8000/ws?token={token}") as ws:
        await ws.send("parece interessante, vou ver esse")
        print(await ws.recv())
        


asyncio.run(test())

