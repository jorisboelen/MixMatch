from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlmodel import Session
from mixmatch.core.settings import settings

engine = create_engine(url=str(settings.sqlalchemy_database_url), pool_size=5, max_overflow=10)
Base = declarative_base()


def get_db():
    with Session(engine) as session:
        yield session
