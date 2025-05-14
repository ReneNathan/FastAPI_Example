from pydantic import BaseModel
from datetime import date


class BorrowalHistoryResponse(BaseModel):
    id: int
    book_id: int
    borrower_id: int
    action: str
    date: date

    class Config:
        orm_mode = True
