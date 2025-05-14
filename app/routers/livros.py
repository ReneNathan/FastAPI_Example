from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.models import Livro, Autor  ##Um livro deve pertencer a um autor
from app.schemas.livro_schema import (
    LivroCreate,
    LivroUpdatePUT,
    LivroResponse,
    LivroUpdatePATCH,
)

router = APIRouter()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get(
    "/",
    response_model=list[LivroResponse],
)
def listar_livros(db: Session = Depends(get_db)):
    livros = db.query(Livro).all()
    return livros


@router.get(
    "/{livro_id}",
    response_model=LivroResponse,
    responses={
        status.HTTP_200_OK: {
            "description": "Livro encontrado com sucesso",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "title": "O instituto",
                        "author_id": 1,
                        "publication_year": "2019",
                        "genre_id": 1,
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
                        "genre_id": 1,
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
            genre_id=livro.genre_id,
            image=livro.image,
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
def atualizar_livro_completo(
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
        livro.genre_id = livro_data.genre_id
        livro.image = livro_data.image

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
def atualizar_livro_parcial(
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


##-----------------------------------------------------------------
##ENDPOINTS ESPECIFICOS


# Endpoint: Buscar livros por ID do autor
@router.get("/autor/id/{autor_id}", response_model=list[dict])
def listar_livros_por_autor_id(autor_id: int, db: Session = Depends(get_db)):
    livros = buscar_livros_por_autor_id(db, autor_id)
    if not livros:
        raise HTTPException(
            status_code=404, detail="Nenhum livro encontrado para este autor."
        )

    return [
        {
            "id": livro.id,
            "titulo": livro.title,
            "ano": livro.publication_year,
            "genero": livro.genre,
            "imagem": livro.image,
        }
        for livro in livros
    ]


# Endpoint: Buscar livros por nome do autor
@router.get("/autor/nome/{nome}", response_model=list[dict])
def listar_livros_por_autor_nome(nome: str, db: Session = Depends(get_db)):
    livros = buscar_livros_por_autor_nome(db, nome)
    if not livros:
        raise HTTPException(
            status_code=404, detail="Nenhum livro encontrado para este autor."
        )

    return [
        {
            "id": livro.id,
            "titulo": livro.title,
            "ano": livro.publication_year,
            "genero": livro.genre,
            "imagem": livro.image,
        }
        for livro in livros
    ]


##----------------------------------------------------------
##FUNÇÕES DOS ENDPOINTS ESPECIFICOS
# Função utilitária: buscar livros por autor_id
def buscar_livros_por_autor_id(db: Session, autor_id: int):
    return db.query(Livro).filter(Livro.author_id == autor_id).all()


# Função utilitária: buscar livros por nome do autor (parcial ou completo)
def buscar_livros_por_autor_nome(db: Session, nome: str):
    return (
        db.query(Livro)
        .join(Autor)
        .filter(
            Autor.name.ilike(f"%{nome}%")
        )  # busca insensível a maiúsculas/minúsculas
        .all()
    )
