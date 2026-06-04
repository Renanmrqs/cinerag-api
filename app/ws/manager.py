from fastapi import  WebSocket
from app.services.chat import positive_movie


class ConnectionManager():
    def __init__(self):
        self.active_connections = {}

    async def connect(self, websocket: WebSocket, username):
        await websocket.accept()
        self.active_connections[username] = websocket

    
    def disconnect(self, websocket: WebSocket, username):
        self.active_connections.pop(username)

    async def broadcast(self, message, username):
        if username in self.active_connections:
            await self.active_connections[username].send_text(message)

    async def send_personal_message(self, message, username):
        print(f"Tentando enviar pra: {username}")
        print(f"Conexões ativas: {self.active_connections.keys()}")
        if username in self.active_connections:
                await self.active_connections[username].send_text(message)
            

    

manager = ConnectionManager()