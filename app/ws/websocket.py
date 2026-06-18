from fastapi import APIRouter, Depends,  WebSocket, WebSocketDisconnect
from app.ws.manager import manager
from app.auth import verify_token
from app.database import get_db
from fastapi import Depends
from sqlalchemy.orm import Session
from app.services.chat_service import service_query

router = APIRouter()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, token: str, db: Session = Depends(get_db)):
    username = verify_token(token)
    await manager.connect(websocket, username)
    try:
        while True:
            data = await websocket.receive_text()
            result = service_query(data, username, db)
            await manager.send_personal_message(f"{result}", username)
    except WebSocketDisconnect:
        manager.disconnect(websocket, username)