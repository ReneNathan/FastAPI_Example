from fastapi import FastAPI
from app.routers import autores, livros, usuarios, emprestimos
from app.database import verificar_conexao

app = FastAPI(
    title="Biblioteca API",
    description="API para gerenciamento de biblioteca",
    version="0.1.0",
)


@app.on_event("startup")
async def startup_event():
    if not verificar_conexao():
        raise RuntimeError("Falha crítica: Banco de dados não disponível")


app.include_router(autores.router, prefix="/api", tags=["autores"])
# app.include_router(livros.router, prefix="/api", tags=["livros"])
# app.include_router(usuarios.router, prefix="/api", tags=["usuarios"])
# app.include_router(emprestimos.router, prefix="/api", tags=["emprestimos"])


@app.get("/")
def root():
    return {"message": "Bem-vindo à Biblioteca API!"}
