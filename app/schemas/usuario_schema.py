from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class UsuarioBase(BaseModel):
    name: str = Field(..., example="João Silva")
    email: EmailStr = Field(..., example="joao@email.com")
    phone: Optional[str] = Field(None, example="(11) 99999-9999")


class UsuarioCreate(UsuarioBase):
    pass


class UsuarioUpdatePUT(UsuarioBase):
    pass


class UsuarioUpdatePATCH(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None


class UsuarioResponse(UsuarioBase):
    id: int

    class Config:
        from_attributes = True
