import asyncio
import websockets

async def test():
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJtYXJsb3MiLCJleHAiOjE3ODA5NzEwNTB9.0S7b4TXZSiUZoxTuT3x-B-3As9_OJmlItrSMnr55xl4"
    async with websockets.connect(f"ws://127.0.0.1:8000/ws?token={token}") as ws:
        await ws.send("opa, gostei desse vou ver e te aviso")
        print(await ws.recv())
        


asyncio.run(test())