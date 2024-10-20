from sqlmodel import SQLModel, Session, create_engine

# fills SQLModel.metadata
from . import models  # noqa: F401

engine = create_engine("")


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
