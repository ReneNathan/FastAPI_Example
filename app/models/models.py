## Criando os modelos
from sqlalchemy import Column, Integer, String, Date, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.database import Base


class Autor(Base):
    __tablename__ = "authors"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    country = Column(String)


class Usuario(Base):
    __tablename__ = "borrowers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    phone = Column(String)


class Livro(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    author_id = Column(Integer, ForeignKey("authors.id"))
    publication_year = Column(Integer)
    genre_id = Column(Integer, ForeignKey("genres.id"))
    image = Column(String)


class Emprestimo(Base):
    __tablename__ = "borrowals"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    borrower_id = Column(Integer, ForeignKey("borrowers.id"), nullable=False)
    borrow_date = Column(Date, nullable=False)
    return_date = Column(Date)


class Genero(Base):  # Ou Genre, como preferir
    __tablename__ = "genres"  # Isso precisa bater com o nome real da tabela no banco

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)


class Stock(Base):
    __tablename__ = "stock"
    book_id = Column(Integer, ForeignKey("books.id"), unique=True, primary_key=True)
    quantity = Column(Integer, default=0)


class Historico_de_emprestimos(Base):
    __tablename__ = "borrowal_history"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    borrower_id = Column(Integer, ForeignKey("borrowers.id"), nullable=False)
    action = Column(String, nullable=False)  # 'borrowed' ou 'returned'
    date = Column(Date, nullable=False)


class Log(Base):
    __tablename__ = "logs"
    id = Column(Integer, primary_key=True, index=True)
    action = Column(String, nullable=False)
    description = Column(String)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
