from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager

from .db import create_db_and_tables
from .egg import init_egg_analyzer


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    init_egg_analyzer()
    yield
