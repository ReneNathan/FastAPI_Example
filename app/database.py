## Tem por objetivo configurar a conexão com o banco de dados

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
import logging
import os.path

# Configurar logging (opcional)
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# SQLALCHEMY_DATABASE_URL = "sqlite:///../database/biblioteca_amostra.db"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_DIR = os.path.join(
    BASE_DIR, "..", "database"
)  # Sobe um nível e entra em "database"
SQLALCHEMY_DATABASE_URL = (
    f"sqlite:///{os.path.join(DATABASE_DIR, 'biblioteca_amostra.db')}"
)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def verificar_conexao():
    """Testa a conexão com o banco de dados"""
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))  # Consulta simples
            logger.info("✅ Conexão com o banco de dados bem-sucedida!")
            return True

    except Exception as e:
        logger.error(f"❌ Falha na conexão com o banco: {str(e)}")
        return False
