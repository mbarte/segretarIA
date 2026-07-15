from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.core.config import settings

# creo collegamento al database
engine = create_engine(
    f"sqlite:///{settings.database_path}",
    connect_args = {
        "check_same_thread": False
    }   
)

# creo sessione di lavoro (apri->r/w->commit->chiudi)
SessionLocal = sessionmaker(
    autocommit = False,
    autoflush = False, 
    bind = engine
)


Base = declarative_base()