from pydantic import BaseModel
from typing import Optional


class AutorCreate(BaseModel):
    name: str
    country: str


class AutorUpdatePUT(BaseModel):
    name: str
    country: str


class AutorUpdatePATCH(BaseModel):
    name: Optional[str] = None
    country: Optional[str] = None
