from pydantic import BaseModel, field_validator, ValidationInfo
from datetime import date
from typing import Optional


class BorrowalBase(BaseModel):
    book_id: int
    borrower_id: int
    borrow_date: date
    return_date: Optional[date] = None

    @field_validator("return_date")
    @classmethod
    def validate_dates(cls, return_date, info: ValidationInfo):
        borrow_date = info.data.get("borrow_date")
        if return_date and borrow_date and return_date < borrow_date:
            raise ValueError(
                "Data de devolução não pode ser anterior à data de empréstimo"
            )
        return return_date


class BorrowalCreate(BorrowalBase):
    pass


class BorrowalUpdatePUT(BorrowalBase):
    pass


class BorrowalUpdatePATCH(BaseModel):
    book_id: Optional[int] = None
    borrower_id: Optional[int] = None
    borrow_date: Optional[date] = None
    return_date: Optional[date] = None


class BorrowalResponse(BaseModel):
    id: int
    book_id: int
    borrower_id: int
    borrow_date: date
    return_date: Optional[date] = None

    model_config = {"from_attributes": True}
