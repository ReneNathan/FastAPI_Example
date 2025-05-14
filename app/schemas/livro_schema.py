from pydantic import BaseModel
from typing import Optional


class LivroCreate(BaseModel):
    title: str
    author_id: int
    publication_year: int
    genre_id: int
    image: str


class LivroUpdatePUT(BaseModel):
    title: str
    author_id: int
    publication_year: int
    genre_id: int
    image: str


class LivroUpdatePATCH(BaseModel):
    title: Optional[str] = None
    author_id: Optional[int] = None
    publication_year: Optional[int] = None
    genre_id: Optional[int] = None
    image: Optional[str]


class LivroResponse(BaseModel):
    id: int
    title: str
    author_id: int
    publication_year: int
    genre_id: int
    image: Optional[str]

    model_config = {"from_attributes": True}
