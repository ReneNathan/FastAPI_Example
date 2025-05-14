from pydantic import BaseModel


class StockBase(BaseModel):
    book_id: int
    quantity: int


class StockCreate(BaseModel):
    book_id: int
    quantity: int


class StockUpdate(BaseModel):
    quantity: int


class StockResponse(StockBase):
    book_id: int
    quantity: int

    class Config:
        orm_mode = True
