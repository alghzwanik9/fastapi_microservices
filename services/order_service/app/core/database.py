from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ...common.utils.database import Base

from .config import get_settings

settings = get_settings()

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Create database tables
Base.metadata.create_all(bind=engine)
