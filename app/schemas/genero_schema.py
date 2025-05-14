from pydantic import BaseModel


class GenreCreate(BaseModel):
    name: str


class GenreResponse(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True
