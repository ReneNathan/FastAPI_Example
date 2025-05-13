from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.models import Livro, Autor  ##Um livro deve pertencer a um autor
from app.schemas.livro_schema import LivroCreate, LivroUpdatePUT, LivroUpdatePATCH

router = APIRouter()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
def listar_livros(db: Session = Depends(get_db)):
    livros = db.query(Livro).all()
    return livros


@router.get(
    "/{livro_id}",
    responses={
        status.HTTP_200_OK: {
            "description": "Livro encontrado com sucesso",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "title": "O instituto",
                        "author_id": "8",
                        "publication_year": "2019",
                        "genre": "Suspense",
                    }
                }
            },
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Livro não encontrado",
            "content": {
                "application/json": {"example": {"detail": "Livro não encontrado"}}
            },
        },
    },
)
def obter_livro(livro_id: int, db: Session = Depends(get_db)):
    livro = db.query(Livro).filter(Livro.id == livro_id).first()
    if not livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    return livro


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {
            "description": "Livro criado com sucesso",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "title": "Dom Casmurro",
                        "author_id": 1,
                        "publication_year": 1899,
                        "genre": "Romance",
                    }
                }
            },
        },
        status.HTTP_400_BAD_REQUEST: {"description": "Dados inválidos"},
        status.HTTP_404_NOT_FOUND: {  # Novo status code adicionado
            "description": "Autor não encontrado",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Um autor com o ID fornecido não foi encontrado"
                    }
                }
            },
        },
    },
)
def criar_livro(livro: LivroCreate, db: Session = Depends(get_db)):
    # Primeiro verifica se o autor existe
    autor = db.query(Autor).filter(Autor.id == livro.author_id).first()

    if not autor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Autor com ID {livro.author_id} não encontrado",
        )

    try:
        novo_livro = Livro(
            title=livro.title,
            author_id=livro.author_id,
            publication_year=livro.publication_year,
            genre=livro.genre,
        )

        db.add(novo_livro)
        db.commit()
        db.refresh(novo_livro)

        return novo_livro

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao criar livro: {str(e)}",
        )


# app/routers/livros.py
@router.put(
    "/{livro_id}",
    responses={
        200: {"description": "Livro atualizado com sucesso"},
        404: {
            "description": "Livro ou autor não encontrado",
            "content": {
                "application/json": {
                    "examples": {
                        "Livro não existe": {
                            "value": {"detail": "Livro com ID 999 não encontrado"}
                        },
                        "Autor não existe": {
                            "value": {"detail": "Autor com ID 888 não encontrado"}
                        },
                    }
                }
            },
        },
    },
)
def atualizar_livro(
    livro_id: int, livro_data: LivroUpdatePUT, db: Session = Depends(get_db)
):
    # Verifica se o livro existe
    livro = db.query(Livro).filter(Livro.id == livro_id).first()
    if not livro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Livro com ID {livro_id} não encontrado",
        )

    # Verifica se o novo autor existe
    autor = db.query(Autor).filter(Autor.id == livro_data.author_id).first()
    if not autor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Autor com ID {livro_data.author_id} não encontrado",
        )

    try:
        # Atualiza todos os campos
        livro.title = livro_data.title
        livro.author_id = livro_data.author_id
        livro.publication_year = livro_data.publication_year
        livro.genre = livro_data.genre

        db.commit()
        db.refresh(livro)

        return livro

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao atualizar livro: {str(e)}",
        )


@router.patch(
    "/{livro_id}",
    responses={
        200: {"description": "Livro parcialmente atualizado"},
        404: {
            "description": "Livro ou autor não encontrado",
            "content": {
                "application/json": {
                    "example": {"detail": "Autor com ID 888 não encontrado"}
                }
            },
        },
    },
)
def atualizar_livro(
    livro_id: int, livro_data: LivroUpdatePATCH, db: Session = Depends(get_db)
):
    livro = db.query(Livro).filter(Livro.id == livro_id).first()
    if not livro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Livro com ID {livro_id} não encontrado",
        )

    # Verifica se o novo autor (se fornecido) existe
    if livro_data.author_id is not None:
        autor = db.query(Autor).filter(Autor.id == livro_data.author_id).first()
        if not autor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Autor com ID {livro_data.author_id} não encontrado",
            )

    try:
        # Atualiza apenas os campos fornecidos
        update_data = livro_data.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(livro, key, value)

        db.commit()
        db.refresh(livro)

        return livro

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao atualizar livro: {str(e)}",
        )


@router.delete(
    "/{livro_id}",
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Livro excluído com sucesso"},
        404: {"description": "Livro não encontrado"},
    },
)
def excluir_livro(livro_id: int, db: Session = Depends(get_db)):
    livro = db.query(Livro).filter(Livro.id == livro_id).first()
    if not livro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Livro com ID {livro_id} não encontrado",
        )

    try:
        db.delete(livro)
        db.commit()
        return {"message": f"Livro {livro_id} excluído com sucesso"}

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao excluir livro: {str(e)}",
        )
