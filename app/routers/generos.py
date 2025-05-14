from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.models import Genero, Livro
from app.schemas.genero_schema import GenreCreate, GenreResponse

router = APIRouter()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Criar gênero
@router.post("/", response_model=GenreResponse, status_code=status.HTTP_201_CREATED)
def criar_genero(genero: GenreCreate, db: Session = Depends(get_db)):
    genero_existente = db.query(Genero).filter(Genero.name == genero.name).first()
    if genero_existente:
        raise HTTPException(status_code=400, detail="Gênero já existe.")

    novo_genero = Genero(name=genero.name)
    db.add(novo_genero)
    db.commit()
    db.refresh(novo_genero)
    return novo_genero


# Listar todos os gêneros
@router.get("/", response_model=list[GenreResponse])
def listar_generos(db: Session = Depends(get_db)):
    return db.query(Genero).all()


# Obter gênero por ID
@router.get("/{genre_id}", response_model=GenreResponse)
def obter_genero(genero_id: int, db: Session = Depends(get_db)):
    genero = db.query(Genero).filter(Genero.id == genero_id).first()
    if not genero:
        raise HTTPException(status_code=404, detail="Gênero não encontrado.")
    return genero


# Atualizar gênero
@router.put("/{genre_id}", response_model=GenreResponse)
def atualizar_genero(
    genero_id: int, genero: GenreCreate, db: Session = Depends(get_db)
):
    genero = db.query(Genero).filter(Genero.id == genero_id).first()
    if not genero:
        raise HTTPException(status_code=404, detail="Gênero não encontrado.")

    genero.name = genero.name
    db.commit()
    db.refresh(genero)
    return genero


# Deletar gênero
@router.delete("/{genre_id}", status_code=status.HTTP_200_OK)
def deletar_genero(genero_id: int, db: Session = Depends(get_db)):
    genero = db.query(Genero).filter(Genero.id == genero_id).first()
    if not genero:
        raise HTTPException(status_code=404, detail="Gênero não encontrado.")

    db.delete(genero)
    db.commit()
    return {"message": f"Gênero {genero_id} excluído com sucesso."}


# Listar livros por gênero
@router.get("/{genre_id}/livros", response_model=list[dict])
def listar_livros_por_genero(genero_id: int, db: Session = Depends(get_db)):
    genero = db.query(Genero).filter(Genero.id == genero_id).first()
    if not genero:
        raise HTTPException(status_code=404, detail="Gênero não encontrado.")

    livros = db.query(Livro).filter(Livro.genre_id == genero_id).all()

    return [
        {
            "id": livro.id,
            "titulo": livro.title,
            "ano": livro.publication_year,
            "autor_id": livro.author_id,
            "imagem": livro.image,
            "genero": genero.name,
        }
        for livro in livros
    ]
