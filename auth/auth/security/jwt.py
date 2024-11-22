from typing import Any, Optional
from datetime import datetime, timedelta, timezone

import jwt

from sqlmodel import Session

from .dto import TokenDTO
from ..settings import (
    SECRET_JWT_PRIVATE_KEY,
    SECRET_JWT_PUBLIC_KEY,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)


def create_jwt_token(username: str, db: Session) -> TokenDTO:
    exp = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token = jwt.encode(
        {"sub": username, "exp": exp},
        SECRET_JWT_PRIVATE_KEY,
        algorithm="RS256",
    )
    return TokenDTO(access_token=token, token_type="bearer", expiration_date=exp)


def decode_token(token: str) -> Any:
    return jwt.decode(token, SECRET_JWT_PUBLIC_KEY, algorithms=["RS256"])
