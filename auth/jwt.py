from datetime import datetime, timedelta, timezone

import jwt


from .models import Token
from .settings import SECRET_JWT_KEY


def create_jwt_token(username: str, expiration: timedelta):
    token = jwt.encode(
        {"sub": username, "exp": datetime.now(timezone.utc) + expiration},
        SECRET_JWT_KEY,
        algorithm="HS256",
    )

    return Token(access_token=token, token_type="bearer")
