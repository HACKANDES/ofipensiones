from datetime import datetime

from sqlmodel import Field, SQLModel


class UserCredentials(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(index=True)
    hashed_password: str
