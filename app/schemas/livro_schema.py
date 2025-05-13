from pydantic import BaseModel
from typing import Optional


class LivroCreate(BaseModel):
    title: str
    author_id: int
    publication_year: int
    genre: str


class LivroUpdatePUT(BaseModel):
    title: str
    author_id: int
    publication_year: int
    genre: str


class LivroUpdatePATCH(BaseModel):
    title: Optional[str] = None
    author_id: Optional[int] = None
    publication_year: Optional[int] = None
    genre: Optional[str] = None
