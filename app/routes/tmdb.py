from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.tmdb import get_films

router = APIRouter()

@router.get("/films/search_film/{film}", tags=['films'])
def get_films_name(film: str):
    film_listed = get_films(film)
    if not film_listed:
        raise HTTPException(status_code=401, detail=f'{film} cannot searched')
    return film_listed


    


