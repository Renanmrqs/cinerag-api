from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.favorites import create_favorite, read_all_favorites
from app.routes.auth import get_current_user
from app.services.auth import get_user_id

router = APIRouter()

@router.post("/films/favorites/post_film", tags=['favorites'])
def post_favorite(movie_id: int, user: str = Depends(get_current_user), db: Session = Depends(get_db)) -> dict:
    user_id = get_user_id(user, db)
    try:
        favorite = create_favorite(user_id, movie_id, db)
        return favorite
    except Exception as e:
        raise HTTPException(status_code=400, detail=f'Unexpected error: {e}')

@router.get("/films/favorites/get_all", tags=['favorites'])
def get_favorites(user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    user_id = get_user_id(user, db)
    try:
        favorite = read_all_favorites(user_id, db)
        return favorite
    except Exception as e:
        raise HTTPException(status_code=400, detail=f'Unexpected error: {e}')