from pydantic import BaseModel

from sqlmodel import Field, SQLModel


class UserBase(SQLModel):
    username: str = Field(index=True)
    email: str | None = Field(default=None, index=True)
    name: str | None = None
    surname: str | None = None


class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str


class Token(BaseModel):
    access_token: str
    token_type: str
