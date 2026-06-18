import asyncio
import websockets

async def test():
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyMjQiLCJ1c2VybmFtZSI6InJlbmFuIiwiZXhwIjoxNzgxNzU2ODA0fQ.kmIKkOCVpAdM61sWLtKxTnLz0Z5iguOFOE6EMN7Q_m4"
    async with websockets.connect(f"ws://127.0.0.1:8000/ws?token={token}") as ws:
        await ws.send("oi recomandame um fiklme")
        print(await ws.recv())
        


asyncio.run(test())

