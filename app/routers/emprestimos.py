from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import date
from app.database import SessionLocal
from app.models.models import Emprestimo, Livro, Usuario
from app.schemas.emprestimo_schema import (
    BorrowalCreate,
    BorrowalUpdatePUT,
    BorrowalUpdatePATCH,
    BorrowalResponse,
)

router = APIRouter()


def get_session_local():
    yield SessionLocal()


# Helper para verificar existência de recursos
def verificar_recurso(db: Session, model, resource_id: int, nome_recurso: str):
    recurso = db.query(model).filter(model.id == resource_id).first()
    if not recurso:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{nome_recurso} com ID {resource_id} não encontrado",
        )
    return recurso


# CREATE
@router.post("/", response_model=BorrowalResponse, status_code=status.HTTP_201_CREATED)
def criar_emprestimo(
    emprestimo: BorrowalCreate, db: Session = Depends(get_session_local)
):
    # Verifica livro
    verificar_recurso(db, Livro, emprestimo.book_id, "Livro")

    # Verifica usuário
    verificar_recurso(db, Usuario, emprestimo.borrower_id, "Usuário")

    try:
        novo_emprestimo = Emprestimo(**emprestimo.model_dump())
        db.add(novo_emprestimo)
        db.commit()
        db.refresh(novo_emprestimo)
        return novo_emprestimo
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao criar empréstimo: {str(e)}",
        )


# READ ALL
@router.get("/", response_model=list[BorrowalResponse])
def listar_emprestimos(db: Session = Depends(get_session_local)):
    return db.query(Emprestimo).all()


# READ BY ID
@router.get("/{emprestimo_id}", response_model=BorrowalResponse)
def obter_emprestimo(emprestimo_id: int, db: Session = Depends(get_session_local)):
    emprestimo = db.query(Emprestimo).filter(Emprestimo.id == emprestimo_id).first()
    if not emprestimo:
        raise HTTPException(status_code=404, detail="Empréstimo não encontrado")
    return emprestimo


# UPDATE (PUT)
@router.put("/{emprestimo_id}", response_model=BorrowalResponse)
def atualizar_emprestimo(
    emprestimo_id: int,
    emprestimo_data: BorrowalUpdatePUT,
    db: Session = Depends(get_session_local),
):
    emprestimo = db.query(Emprestimo).filter(Emprestimo.id == emprestimo_id).first()
    if not emprestimo:
        raise HTTPException(status_code=404, detail="Empréstimo não encontrado")

    # Verificações
    verificar_recurso(db, Livro, emprestimo_data.book_id, "Livro")
    verificar_recurso(db, Usuario, emprestimo_data.borrower_id, "Usuário")

    try:
        # Use uma abordagem alternativa com update()
        db.query(Emprestimo).filter(Emprestimo.id == emprestimo_id).update(
            {
                Emprestimo.book_id: emprestimo_data.book_id,
                Emprestimo.borrower_id: emprestimo_data.borrower_id,
                Emprestimo.borrow_date: emprestimo_data.borrow_date,
                Emprestimo.return_date: emprestimo_data.return_date,
            }
        )

        db.commit()
        db.refresh(emprestimo)
        return emprestimo
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar: {str(e)}")


# UPDATE (PATCH)
@router.patch("/{emprestimo_id}", response_model=BorrowalResponse)
def atualizar_emprestimo(
    emprestimo_id: int,
    emprestimo_data: BorrowalUpdatePATCH,
    db: Session = Depends(get_session_local),
):
    emprestimo = db.query(Emprestimo).filter(Emprestimo.id == emprestimo_id).first()
    if not emprestimo:
        raise HTTPException(status_code=404, detail="Empréstimo não encontrado")

    update_data = emprestimo_data.model_dump(exclude_unset=True)

    # Verifica chaves estrangeiras se fornecidas
    if "book_id" in update_data:
        verificar_recurso(db, Livro, update_data["book_id"], "Livro")
    if "borrower_id" in update_data:
        verificar_recurso(db, Usuario, update_data["borrower_id"], "Usuário")

    try:
        for key, value in update_data.items():
            setattr(emprestimo, key, value)

        db.commit()
        db.refresh(emprestimo)
        return emprestimo
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar: {str(e)}")


# DELETE
@router.delete("/{emprestimo_id}", status_code=status.HTTP_200_OK)
def excluir_emprestimo(emprestimo_id: int, db: Session = Depends(get_session_local)):
    emprestimo = db.query(Emprestimo).filter(Emprestimo.id == emprestimo_id).first()
    if not emprestimo:
        raise HTTPException(status_code=404, detail="Empréstimo não encontrado")

    try:
        db.delete(emprestimo)
        db.commit()
        return {"message": "Empréstimo excluído com sucesso"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao excluir: {str(e)}")


@router.get("/por-usuario/{usuario_id}", response_model=list[BorrowalResponse])
def listar_emprestimos_por_usuario(
    usuario_id: int, db: Session = Depends(get_session_local)
):
    emprestimos = (
        db.query(Emprestimo).filter(Emprestimo.borrower_id == usuario_id).all()
    )

    if not emprestimos:
        raise HTTPException(
            status_code=404, detail="Nenhum empréstimo encontrado para este usuário."
        )

    return emprestimos
