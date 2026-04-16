import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

def _build_url():
    # Direct URL takes priority
    url = os.environ.get("DATABASE_URL") or os.environ.get("POSTGRES_URI")
    if url:
        return url
    # Zeabur individual vars
    host = os.environ.get("POSTGRES_HOST", "")
    port = os.environ.get("POSTGRES_PORT", "5432")
    user = os.environ.get("POSTGRES_USERNAME") or os.environ.get("POSTGRES_USER", "")
    password = os.environ.get("POSTGRES_PASSWORD", "")
    db = os.environ.get("POSTGRES_DB") or os.environ.get("POSTGRES_DATABASE", "")
    if host and user and db:
        return f"postgresql://{user}:{password}@{host}:{port}/{db}"
    return "postgresql://user:password@localhost:5432/covora"

DATABASE_URL = _build_url()

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
