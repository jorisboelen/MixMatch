from fastapi import APIRouter, Depends
from mixmatch.db.database import get_db
from sqlmodel import Session, text

router = APIRouter()


@router.get("/health", status_code=200)
def health_check(db: Session = Depends(get_db)):
    db.execute(text("""SELECT 1""")).one()
    return {'status': 'ok'}
