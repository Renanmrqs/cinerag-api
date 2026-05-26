from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.tmdb import get_films, get_film_score
from app.routes.auth import get_current_user

router = APIRouter()

@router.get("/films/search_film/{film_name}", tags=['films'])
def get_films_name(film_name: str, user: str = Depends(get_current_user)) -> list:
    film_listed = get_films(film_name)
    if not film_listed:
        raise HTTPException(status_code=404, detail=f'{film_name} cannot searched')
    return film_listed

@router.get("/films/get_score/{film_id}", tags=['films'])
def get_film_score_route(film_id: int, db: Session = Depends(get_db), user: str = Depends(get_current_user)) -> dict:
    try:
        film_score = get_film_score(film_id, db)
        return film_score
    except Exception as e:
        raise HTTPException(status_code=404, detail=f'Unexpectded error: {str(e)}')
        
