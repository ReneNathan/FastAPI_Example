from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.models import Usuario
from app.schemas.usuario_schema import (
    UsuarioCreate,
    UsuarioUpdatePUT,
    UsuarioUpdatePATCH,
    UsuarioResponse,
)

router = APIRouter()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get(
    "/",
    response_model=list[UsuarioResponse],
    responses={
        status.HTTP_200_OK: {
            "description": "Lista de usuários retornada com sucesso",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": 1,
                            "name": "João Silva",
                            "email": "joao@email.com",
                            "phone": "(11) 9999-1111",
                        }
                    ]
                }
            },
        }
    },
)
def listar_usuarios(db: Session = Depends(get_db)):
    usuarios = db.query(Usuario).all()
    return usuarios


@router.get(
    "/{usuario_id}",
    response_model=UsuarioResponse,
    responses={
        status.HTTP_200_OK: {
            "description": "Usuário encontrado com sucesso",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "name": "João Silva",
                        "email": "joao@email.com",
                        "phone": "(11) 9999-1111",
                    }
                }
            },
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Usuário não encontrado",
            "content": {
                "application/json": {"example": {"detail": "Usuário não encontrado"}}
            },
        },
    },
)
def obter_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado"
        )
    return usuario


@router.post(
    "/",
    response_model=UsuarioResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {
            "description": "Usuário criado com sucesso",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "name": "João Silva",
                        "email": "joao@email.com",
                        "phone": "(11) 9999-1111",
                    }
                }
            },
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "Dados inválidos ou email já cadastrado",
            "content": {
                "application/json": {"example": {"detail": "Email já está em uso"}}
            },
        },
    },
)
def criar_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    # Verifica se email já existe
    if db.query(Usuario).filter(Usuario.email == usuario.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email já está em uso"
        )

    try:
        novo_usuario = Usuario(
            name=usuario.name,
            email=usuario.email,
            phone=usuario.phone,
        )

        db.add(novo_usuario)
        db.commit()
        db.refresh(novo_usuario)

        return novo_usuario

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao criar usuário: {str(e)}",
        )


@router.put(
    "/{usuario_id}",
    response_model=UsuarioResponse,
    responses={
        status.HTTP_200_OK: {
            "description": "Usuário atualizado com sucesso",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "name": "João Silva",
                        "email": "joao.novo@email.com",
                        "phone": "(11) 9999-0000",
                    }
                }
            },
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Usuário não encontrado",
            "content": {
                "application/json": {"example": {"detail": "Usuário não encontrado"}}
            },
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "Email já está em uso",
            "content": {
                "application/json": {"example": {"detail": "Email já está em uso"}}
            },
        },
    },
)
def atualizar_usuario(
    usuario_id: int, usuario_data: UsuarioUpdatePUT, db: Session = Depends(get_db)
):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado"
        )

    # Verifica se novo email já existe
    if usuario_data.email != usuario.email:
        if db.query(Usuario).filter(Usuario.email == usuario_data.email).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Email já está em uso"
            )

    try:
        usuario.name = usuario_data.name
        usuario.email = usuario_data.email
        usuario.phone = usuario_data.phone

        db.commit()
        db.refresh(usuario)

        return usuario

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao atualizar usuário: {str(e)}",
        )


@router.patch(
    "/{usuario_id}",
    response_model=UsuarioResponse,
    responses={
        status.HTTP_200_OK: {
            "description": "Usuário parcialmente atualizado",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "name": "João Silva",
                        "email": "joao@email.com",
                        "phone": "(11) 9999-0000",
                    }
                }
            },
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Usuário não encontrado",
            "content": {
                "application/json": {"example": {"detail": "Usuário não encontrado"}}
            },
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "Email já está em uso",
            "content": {
                "application/json": {"example": {"detail": "Email já está em uso"}}
            },
        },
    },
)
def atualizar_usuario(
    usuario_id: int, usuario_data: UsuarioUpdatePATCH, db: Session = Depends(get_db)
):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado"
        )

    update_data = usuario_data.dict(exclude_unset=True)

    # Verifica se novo email (se fornecido) já existe
    if "email" in update_data and update_data["email"] != usuario.email:
        if db.query(Usuario).filter(Usuario.email == update_data["email"]).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Email já está em uso"
            )

    try:
        for key, value in update_data.items():
            setattr(usuario, key, value)

        db.commit()
        db.refresh(usuario)

        return usuario

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao atualizar usuário: {str(e)}",
        )


@router.delete(
    "/{usuario_id}",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            "description": "Usuário excluído com sucesso",
            "content": {
                "application/json": {"example": {"message": "Usuário excluído"}}
            },
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Usuário não encontrado",
            "content": {
                "application/json": {"example": {"detail": "Usuário não encontrado"}}
            },
        },
    },
)
def excluir_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado"
        )

    try:
        db.delete(usuario)
        db.commit()
        return {"message": "Usuário excluído com sucesso"}

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao excluir usuário: {str(e)}",
        )
