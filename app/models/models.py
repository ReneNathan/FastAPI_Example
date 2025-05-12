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
    book_id = Column(Integer, ForeignKey("books.id"))
    borrower_id = Column(Integer, ForeignKey("borrower_id"))
    borrow_date = Column(String)
    return_date = Column(String)
