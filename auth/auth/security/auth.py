from typing import Annotated, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from sqlmodel import Session, select

from passlib.hash import argon2

from jwt import InvalidTokenError

from ..db import get_session
from .dto import UserRegistrationDTO
from .models import UserCredentials as Credentials
from .jwt import decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_token(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[Session, Depends(get_session)],
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode_token(token)
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception

    stmt = select(Credentials.username).where(Credentials.username == username)
    if db.exec(stmt).one_or_none() is None:
        raise credentials_exception


def authenticate(username: str, password: str, db: Session) -> Optional[Credentials]:
    hashed_password = argon2.hash(password)

    stmt = select(Credentials).where(
        Credentials.username == username
        and Credentials.hashed_password == hashed_password
    )
    return db.exec(stmt).one_or_none()


def query_token_user(username: str, db: Session) -> Optional[str]:
    stmt = select(Credentials.username).where(Credentials.username == username)
    db.exec(stmt).one_or_none()


def register(user: UserRegistrationDTO, db: Session):
    stmt = select(Credentials.id).where(Credentials.username == user.username)
    if db.exec(stmt).one_or_none() is not None:
        return {"username": user.username, "status": "ALREADY_EXISTS"}

    c = Credentials(username=user.username, hashed_password=argon2.hash(user.password))
    db.add(c)
    db.commit()
