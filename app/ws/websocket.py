from fastapi import APIRouter, Depends,  WebSocket, WebSocketDisconnect
from app.ws.manager import manager
from app.auth import verify_token
from app.database import get_db
from fastapi import Depends
from sqlalchemy.orm import Session
from app.services.chat import positive_movie, smaller_trusted, most_trusted, negative_movie, mixed_movie, count_films, first_added, last_added
from app.services.gemini import gemini_func

router = APIRouter()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, token: str, db: Session = Depends(get_db)):
    username = verify_token(token)
    await manager.connect(websocket, username)
    try:
        while True:
            data = await websocket.receive_text()
            if data == '/positives':
                result = positive_movie(username, db)
                await manager.send_personal_message(result, username)
            elif data == '/negatives':
                result = negative_movie(username, db)
                await manager.send_personal_message(result, username)
            elif data == '/mixeds':
                result = mixed_movie(username, db)
                await manager.send_personal_message(result, username)
            elif data == '/most trusted':
                result = most_trusted(username, db)
                await manager.send_personal_message(result, username)
            elif data == '/count films':
                result = count_films(username, db)
                await manager.send_personal_message(result, username)
            elif data == '/smaller trusted':
                result = smaller_trusted(username, db)
                await manager.send_personal_message(result, username)
            elif data == '/first film added':
                result = first_added(username, db)
                await manager.send_personal_message(result, username)
            elif data == '/last film added':
                result = last_added(username, db)
                await manager.send_personal_message(result, username)
            else:
                result = gemini_func(username, data, db)
                await manager.send_personal_message(f"{result}", username)
    except WebSocketDisconnect:
        manager.disconnect(websocket)