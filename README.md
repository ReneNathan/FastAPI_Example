# EXEMPLO/Material de Estudo - FastAPI - Sistema de Gerenciamento de Biblioteca

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.68.0-green)](https://fastapi.tiangolo.com/)

API CRUD para gestão de livros em uma biblioteca, desenvolvida com FastAPI e SQLite. Tem por objetivo servir como material para estudos de desenvolvimento de APIs RESTful.

## 📚 Recursos Esperados
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
```

🗄️ Estrutura do Banco de Dados
 <br>Diagrama do Banco de Dados

![database_diagram](https://github.com/user-attachments/assets/cf52434a-fd5c-410c-80ee-7c27960d2357)

<br> O banco de dados encontra-se integrado ao projeto, não sendo necessária sua criação manual. Entretanto, caso seja necessário recriá-lo, execute o seguinte comando:

```bash
sqlite3 biblioteca.db < sqlite_script.txt
```

📄 Licença
 <br>Sem licença - Livre uso - Criado como material de estudo

## 🐛 Problemas Conhecidos

### Bloqueio de Porta após Encerramento Improprio

#### Descrição
Se a API não for encerrada corretamente (ex.: usando `Ctrl+C` no terminal), o processo pode permanecer ativo bloqueando a porta utilizada (normalmente 8000). Isso impede a reinicialização da API ou de qualquer outra aplicação que use a mesma porta.

---

#### Solução para Windows
**Passo 1 - Identificar o processo:**
```bash
netstat -aon | findstr :8000
```
*Observação:* Localize o número **PID** na última coluna do resultado.

**Passo 2 - Encerrar o processo:**
```bash
taskkill /PID <NÚMERO_PID> /F
```

---

#### Solução para Linux/macOS
**Passo 1 - Encontrar o processo:**
```bash
lsof -i :8000
```

**Passo 2 - Encerrar o processo:**
```bash
kill -9 <NÚMERO_PID>
```

---

#### Prevenção
- ⚠️ Sempre encerre a API com `Ctrl+C` no terminal
- 🛠️ Use ferramentas como `nodemon` (Node.js) para reinicialização automática
- 🔍 Implemente scripts que verifiquem portas bloqueadas antes da inicialização

---

#### Solução Automática (Windows)
Para encerrar todos os processos na porta 8000 automaticamente:
```bash
for /f "tokens=5" %a in ('netstat -aon ^| findstr :8000') do taskkill /PID %a /F
```

---

#### Exemplo Prático
**Saída do `netstat` no Windows:**
```bash
TCP    0.0.0.0:8000           0.0.0.0:0              LISTENING       12345
```
*Neste caso:* `12345` é o PID a ser usado no `taskkill`.

---

#### Troubleshooting Avançado
**Verificar todas as portas em uso:**
```bash
# Windows
netstat -aon

# Linux/macOS
sudo lsof -i -P -n
```

> **Nota Importante:** Substitua `8000` pela porta real do seu projeto em todos os comandos!