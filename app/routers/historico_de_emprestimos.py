from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Literal
from app.models.models import Historico_de_emprestimos
from app.schemas.historico_de_emprestimos_schema import BorrowalHistoryResponse
from app.database import SessionLocal

router = APIRouter()


def get_session_local():
    yield SessionLocal()


@router.get("/", response_model=List[BorrowalHistoryResponse])
def listar_historico(
    action: Literal["all", "borrowed", "returned"] = Query("all"),
    db: Session = Depends(get_session_local),
):
    query = db.query(Historico_de_emprestimos)
    if action != "all":
        query = query.filter(Historico_de_emprestimos.action == action)
    return query.all()


@router.get("/{history_id}", response_model=BorrowalHistoryResponse)
def obter_registro_por_id(history_id: int, db: Session = Depends(get_session_local)):
    registro = (
        db.query(Historico_de_emprestimos)
        .filter(Historico_de_emprestimos.id == history_id)
        .first()
    )
    if not registro:
        raise HTTPException(status_code=404, detail="Registro não encontrado")
    return registro


@router.get("/book/{book_id}", response_model=List[BorrowalHistoryResponse])
def historico_por_livro(
    book_id: int,
    action: Literal["all", "borrowed", "returned"] = Query("all"),
    db: Session = Depends(get_session_local),
):
    query = db.query(Historico_de_emprestimos).filter(
        Historico_de_emprestimos.book_id == book_id
    )
    if action != "all":
        query = query.filter(Historico_de_emprestimos.action == action)
    return query.all()


@router.get("/user/{user_id}", response_model=List[BorrowalHistoryResponse])
def historico_por_usuario(
    user_id: int,
    action: Literal["all", "borrowed", "returned"] = Query("all"),
    db: Session = Depends(get_session_local),
):
    query = db.query(Historico_de_emprestimos).filter(
        Historico_de_emprestimos.borrower_id == user_id
    )
    if action != "all":
        query = query.filter(Historico_de_emprestimos.action == action)
    return query.all()
