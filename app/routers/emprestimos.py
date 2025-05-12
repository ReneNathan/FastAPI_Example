from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.models import Emprestimo

router = APIRouter()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
def listar_emprestimos(db: Session = Depends(get_db)):
    emprestimo = db.query(Emprestimo).all()
    return emprestimo
