from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.models import Stock, Livro
from app.schemas.stock_schema import StockResponse, StockCreate, StockUpdate

router = APIRouter()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=list[StockResponse])
def listar_estoque(db: Session = Depends(get_db)):
    return db.query(Stock).all()


@router.get("/livro/{book_id}", response_model=StockResponse)
def obter_estoque_por_livro(book_id: int, db: Session = Depends(get_db)):
    # Verifica se o livro existe
    livro = db.query(Livro).filter(Livro.id == book_id).first()
    if not livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado.")

    # Busca o estoque relacionado ao livro
    estoque = db.query(Stock).filter(Stock.book_id == book_id).first()
    if not estoque:
        raise HTTPException(
            status_code=404, detail="Estoque não encontrado para este livro."
        )

    return estoque


@router.post("/", response_model=StockResponse, status_code=201)
def criar_estoque(stock: StockCreate, db: Session = Depends(get_db)):
    # Verifica se o livro existe
    livro = db.query(Livro).filter(Livro.id == stock.book_id).first()
    if not livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado.")

    # Verifica se já existe estoque para esse livro
    db_estoque = db.query(Stock).filter(Stock.book_id == stock.book_id).first()
    if db_estoque:
        raise HTTPException(
            status_code=400, detail="Estoque já cadastrado para este livro."
        )

    # Cria o novo estoque
    novo_estoque = Stock(**stock.dict())
    db.add(novo_estoque)
    db.commit()
    db.refresh(novo_estoque)
    return novo_estoque


@router.put("/{book_id}", response_model=StockResponse)
def atualizar_estoque(book_id: int, dados: StockUpdate, db: Session = Depends(get_db)):
    estoque = db.query(Stock).filter(Stock.book_id == book_id).first()
    if not estoque:
        raise HTTPException(status_code=404, detail="Estoque não encontrado.")

    estoque.quantity = dados.quantity
    db.commit()
    db.refresh(estoque)
    return estoque
