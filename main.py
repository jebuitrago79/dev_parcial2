from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.params import Depends

from utils.connection_db import init_db, get_session
from data.models import usuario
from sqlmodel.ext.asyncio.session import AsyncSession


@asynccontextmanager
async def lifespan(app:FastAPI):
    await init_db()
    yield
app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

@app.post("/usuario")
async def crear_usuario( nuevo_usuario: usuario, session: AsyncSession = Depends(get_session)):
    session.add(nuevo_usuario)
    await session.commit()
    await session.refresh(nuevo_usuario)
    return nuevo_usuario


