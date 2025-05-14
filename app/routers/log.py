from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.models import Log
from app.schemas.log_schema import LogResponse
from typing import List

router = APIRouter()


def get_session_local():
    yield SessionLocal()


@router.get("/", response_model=List[LogResponse])
def listar_logs(db: Session = Depends(get_session_local)):
    return db.query(Log).order_by(Log.timestamp.desc()).all()
