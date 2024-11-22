from typing import Annotated

from fastapi import Depends, FastAPI, Form, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from jwt import InvalidTokenError
from sqlmodel import Session


from .db import get_session
from .egg import easter_egg
from .lifespan import lifespan

from .security import auth
from .security.jwt import create_jwt_token
from .security.dto import UserRegistrationDTO, TokenDTO

app = FastAPI(lifespan=lifespan)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.get("/healthcheck")
async def healthcheck():
    return {"status": "OK"}


@app.post("/token")
async def login_for_access_token(
    data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(get_session)],
) -> TokenDTO:
    user = auth.authenticate(data.username, data.password, db)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return create_jwt_token(data.username, db)


async def get_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[Session, Depends(get_session)],
) -> str:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = auth.decode_token(token)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception

    if auth.query_token_user(username, db) is None:
        raise credentials_exception

    return username


@app.get("/users/me/")
async def users_me(username: Annotated[str, Depends(get_user)]):
    return {"username": username}


@app.post("/register/")
async def register(
    user: Annotated[UserRegistrationDTO, Form()],
    db: Annotated[Session, Depends(get_session)],
):
    auth.register(user, db)

    return {"username": user.username, "status": "REGISTER_SUCCESS"}


@app.get("/egg/")
async def egg(msg: str):
    return {"message": easter_egg(msg)}
