## Criando os modelos
from sqlalchemy import Column, Integer, String, Date, ForeignKey
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
    genre = Column(String)


class Emprestimo(Base):
    __tablename__ = "borrowals"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    borrower_id = Column(Integer, ForeignKey("borrowers.id"), nullable=False)
    borrow_date = Column(Date, nullable=False)
    return_date = Column(Date)
