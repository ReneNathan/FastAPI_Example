from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.models import Autor
from app.schemas.autor_schema import AutorCreate, AutorUpdatePATCH, AutorUpdatePUT

# router = APIRouter(prefix="/autores", tags="AUTORES")
router = APIRouter()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
def listar_autores(db: Session = Depends(get_db)):
    autores = db.query(Autor).all()
    return autores


@router.get(
    "/{autor_id}",
    responses={
        status.HTTP_200_OK: {
            "description": "Autor encontrado com sucesso",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "name": "Machado de Assis",
                        "country": "Brasil",
                    }
                }
            },
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Autor não encontrado",
            "content": {
                "application/json": {"example": {"detail": "Autor não encontrado"}}
            },
        },
    },
)
def obter_autor(autor_id: int, db: Session = Depends(get_db)):
    autor = db.query(Autor).filter(Autor.id == autor_id).first()
    if not autor:
        raise HTTPException(status_code=404, detail="Autor não encontrado")
    return autor


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {
            "description": "Autor criado com sucesso",
            "content": {
                "application/json": {
                    "example": {"id": 7, "name": "Novo Autor", "country": "Brasil"}
                }
            },
        },
        status.HTTP_400_BAD_REQUEST: {"description": "Dados inválidos"},
    },
)
def criar_autor(autor: AutorCreate, db: Session = Depends(get_db)):
    try:
        novo_autor = Autor(name=autor.name, country=autor.country)

        db.add(novo_autor)
        db.commit()
        db.refresh(novo_autor)

        return novo_autor

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao criar autor: {str(e)}",
        )


@router.put(
    "/{autor_id}",
    responses={
        200: {"description": "Autor atualizado com sucesso"},
        404: {"description": "Autor não encontrado"},
        400: {"description": "Dados inválidos"},
    },
)
def atualizar_autor(
    autor_id: int, autor_data: AutorUpdatePUT, db: Session = Depends(get_db)
):
    """
    Atualiza **todos** os campos de um autor
    """

    autor = db.query(Autor).filter(Autor.id == autor_id).first()
    if not autor:
        raise HTTPException(status_code=404, detail="Autor não encontrado")

    try:
        autor.name = autor_data.name
        autor.country = autor_data.country

        db.commit()
        db.refresh(autor)

        return autor

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Erro na atualização: {str(e)}")


@router.patch(
    "/{autor_id}",
    responses={
        200: {"description": "Autor parcialmente atualizado"},
        404: {"description": "Autor não encontrado"},
        400: {"description": "Dados inválidos ou nenhum campo para atualizar"},
    },
)
def atualizar_autor(
    autor_id: int, autor_data: AutorUpdatePATCH, db: Session = Depends(get_db)
):
    """
    Atualiza **apenas alguns campos** de um autor
    """

    # Busca o autor
    autor = db.query(Autor).filter(Autor.id == autor_id).first()
    if not autor:
        raise HTTPException(status_code=404, detail="Autor não encontrado")

    # Verifica se há campos para atualizar
    update_data = autor_data.dict(exclude_unset=True)
    if not update_data:
        raise HTTPException(
            status_code=400, detail="Nenhum campo fornecido para atualização"
        )

    try:
        # Atualiza apenas os campos enviados
        for key, value in update_data.items():
            setattr(autor, key, value)

        db.commit()
        db.refresh(autor)

        return autor

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Erro na atualização: {str(e)}")


@router.delete(
    "/{autor_id}",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            "description": "Autor excluído com sucesso",
            "content": {"application/json": {"example": {"message": "Autor excluído"}}},
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Autor não encontrado",
            "content": {
                "application/json": {"example": {"detail": "Autor não encontrado"}}
            },
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "Autor possui livros vinculados",
            "content": {
                "application/json": {
                    "example": {"detail": "Autor possui livros vinculados"}
                }
            },
        },
    },
)
def excluir_autor(autor_id: int, db: Session = Depends(get_db)):
    """
    Exclui um autor pelo ID.
    """
    # Busca o autor no banco
    autor = db.query(Autor).filter(Autor.id == autor_id).first()

    if not autor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Autor não encontrado"
        )

    try:
        db.delete(autor)
        db.commit()
        return {"message": "Autor excluído com sucesso"}

    except Exception as e:
        db.rollback()
        if "locked" in str(e):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Autor possui livros vinculados",
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro ao excluir autor: {str(e)}",
            )
