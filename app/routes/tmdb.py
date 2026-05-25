from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.tmdb import get_films, get_film_score

router = APIRouter()

@router.get("/films/search_film/{film}", tags=['films'])
def get_films_name(film: str) -> dict:
    film_listed = get_films(film)
    if not film_listed:
        raise HTTPException(status_code=401, detail=f'{film} cannot searched')
    return film_listed

@router.get("/films/get_score/{film_id}", tags=['films'])
def get_film_score_route(film_id: int, db: Session = Depends(get_db)) -> dict:
    film_score = get_film_score(film_id, db)
    if not film_score:
        raise HTTPException(status_code=401, detail=f'this movie cannot searched')
    return film_score

