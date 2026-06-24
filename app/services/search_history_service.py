from app.models import SearchHistory
from sqlalchemy.orm import Session
from datetime import date
from app.core.logging import logger

def add_user_history(user_id, query, db: Session):
    try:
        add = SearchHistory(user_id=user_id, query=query, searched_at=date.today())
        db.add(add)
        db.commit()
        db.refresh(add)
        return {'message': 'quey saved!'}
    except Exception as e:
        logger.error(f"Save Chat error: {e}")
        raise