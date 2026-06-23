import asyncio
import websockets

async def test():
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMzQiLCJ1c2VybmFtZSI6Ikdlb21hIiwiZXhwIjoxNzgyMjYwNDc3fQ.Lav6tQa3x2950ndSDRfLkSWQs6TaV6_Qu2WQzGvov7A"
    async with websockets.connect(f"ws://127.0.0.1:8000/ws?token={token}") as ws:
        await ws.send("amigo, vou querer uma recomendacao hoje")
        print(await ws.recv())
        


asyncio.run(test())

