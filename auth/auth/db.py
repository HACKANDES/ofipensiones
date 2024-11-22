from sqlmodel import SQLModel, Session, create_engine

# fills SQLModel.metadata
from .security import models  # noqa: F401
from .settings import DB_URI, DB_MIGRATION_URI


engine = create_engine(DB_URI)


def create_db_and_tables():
    migration_engine = create_engine(DB_MIGRATION_URI)
    SQLModel.metadata.create_all(migration_engine)


def get_session():
    with Session(engine) as session:
        yield session
