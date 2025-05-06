from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Body
from fastapi.params import Depends
from sqlmodel import select
from utils.connection_db import init_db, get_session
from data.models import usuario
from sqlmodel.ext.asyncio.session import AsyncSession
from operations.operations_db import actualizar_usuario, hacer_usuario_premium, obtener_usuarios_activos


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

@app.post("/usuarios")
async def crear_usuario( nuevo_usuario: usuario, session: AsyncSession = Depends(get_session)):
    session.add(nuevo_usuario)
    await session.commit()
    await session.refresh(nuevo_usuario)
    return nuevo_usuario

@app.get("/usuarios")
async def obtener_usuarios(session: AsyncSession = Depends(get_session)):
    consulta = select(usuario)
    resultado = await session.exec(consulta)
    usuarios = resultado.all()
    return usuarios


@app.put("/usuarios/{usuario_id}")
async def actualizar(usuario_id: int,datos: usuario = Body(...),session: AsyncSession = Depends(get_session)):
    usuario_actualizado = await actualizar_usuario(usuario_id, datos.dict(exclude_unset=True), session)
    if not usuario_actualizado:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario_actualizado


@app.patch("/usuarios/{usuario_id}/premium")
async def marcar_premium(usuario_id: int, session: AsyncSession = Depends(get_session)):
    usuario_actualizado = await hacer_usuario_premium(usuario_id, session)
    if not usuario_actualizado:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario_actualizado

@app.get("/usuarios/activos")
async def listar_activos(session: AsyncSession = Depends(get_session)):
    return await obtener_usuarios_activos(session)

@app.get("/usuarios/{usuario_id}")
async def obtener_usuario(usuario_id: int, session: AsyncSession = Depends(get_session)):
    consulta = select(usuario).where(usuario.id == usuario_id)
    resultado = await session.exec(consulta)
    encontrado = resultado.first()
    if not encontrado:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return encontrado

