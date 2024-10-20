from passlib.hash import argon2

from sqlmodel import Session, select

from .models import User


def authenticate(username: str, password: str, session: Session):
    hashed_password = argon2.hash(password)

    stmt = select(User).where(
        User.username == username and User.hashed_password == hashed_password
    )
    return session.exec(stmt).one()
