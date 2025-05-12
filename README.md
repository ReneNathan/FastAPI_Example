# EXEMPLO/Material de Estudo - FastAPI - Sistema de Gerenciamento de Biblioteca

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.68.0-green)](https://fastapi.tiangolo.com/)

API CRUD para gestão de livros em uma biblioteca, desenvolvida com FastAPI e SQLite. Tem por objetivo servir como material para estudos de desenvolvimento de APIs RESTful.

## 📚 Recursos
- Operações CRUD
- Banco de dados SQLite integrado
- Documentação interativa com Swagger UI e ReDoc
- Pronto para deploy em produção
- Esquema de dados relacional
- Validação de dados com Pydantic

## 🌐 API Publicada
A API está hospedada no **Heroku** e pode ser acessada diretamente:  
🔗 [Documentação Interativa](https://api-bibliote-estudo-crud-ac46c8c9300f.herokuapp.com/docs)  
🔗 [Documentação ReDoc](https://api-bibliote-estudo-crud-ac46c8c9300f.herokuapp.com/redoc)

## 💻 Uso Local

### Pré-requisitos
- Python 3.9+
- pip
- SQLite3

### Instalação
```bash
# 1. Clonar repositório
git clone https://github.com/seu-usuario/api-biblioteca.git
cd api-biblioteca

# 2. Criar ambiente virtual
python -m venv venv

# 3. Ativar ambiente
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 4. Instalar dependências
pip install -r requirements.txt

# 5. Executar aplicação
uvicorn app.main:app --reload
Acesse a documentação local:
http://localhost:8000/docs
http://localhost:8000/redoc
```

🗄️ Estrutura do Banco de Dados
 <br>Diagrama do Banco de Dados

![database_diagram](https://github.com/user-attachments/assets/cf52434a-fd5c-410c-80ee-7c27960d2357)

<br> O banco de dados se encontra acoplado ao projeto, não sendo necessário sua criação. mas caso necessite recria-lo basta utilizar o seguinte comando:

```bash
sqlite3 biblioteca.db < sqlite_script.txt
```

📄 Licença
 <br>Sem licença - Livre uso - Criado como material de estudo
