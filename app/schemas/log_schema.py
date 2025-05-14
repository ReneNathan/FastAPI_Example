from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class LogResponse(BaseModel):
    id: int
    action: str
    description: Optional[str]
    timestamp: datetime

    class Config:
        orm_mode = True
