from fastapi import FastAPI
from app.routers import autores, livros, usuarios, emprestimos
from app.database import verificar_conexao

app = FastAPI(
    title="Biblioteca API",
    description=(
        "API básica em Python utilizando FastAPI.\n\n"
        "Tem como objetivo servir como material de estudo, simulando uma API de controle de fluxo de uma biblioteca.\n\n"
        "[Repositório no GitHub](https://github.com/ReneNathan/FastAPI_Example)"
    ),
    version="1.0.0",
)


@app.on_event("startup")
async def startup_event():
    if not verificar_conexao():
        raise RuntimeError("Falha crítica: Banco de dados não disponível")


app.include_router(autores.router, prefix="/api/autores", tags=["AUTORES"])
app.include_router(livros.router, prefix="/api/livros", tags=["LIVROS"])
app.include_router(usuarios.router, prefix="/api/usuarios", tags=["USUARIOS"])
app.include_router(emprestimos.router, prefix="/api/emprestimos", tags=["EMPRESTIMOS"])


@app.get("/")
def root():
    return {"message": "Bem-vindo à Biblioteca API!"}
