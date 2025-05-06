from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Body
from fastapi.params import Depends
from sqlmodel import select
from utils.connection_db import init_db, get_session
from data.models import usuario, tarea,EstadoTarea
from sqlmodel.ext.asyncio.session import AsyncSession
from operations.operations_db import actualizar_usuario, hacer_usuario_premium, obtener_usuarios_activos, obtener_usuarios_premium_activos, obtener_todas_las_tareas, obtener_tarea_por_id, actualizar_estado_tarea
from datetime import datetime

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

@app.get("/usuarios/premium-activos")
async def listar_premium_activos(session: AsyncSession = Depends(get_session)):
    return await obtener_usuarios_premium_activos(session)

@app.get("/usuarios/{usuario_id}")
async def obtener_usuario(usuario_id: int, session: AsyncSession = Depends(get_session)):
    consulta = select(usuario).where(usuario.id == usuario_id)
    resultado = await session.exec(consulta)
    encontrado = resultado.first()
    if not encontrado:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return encontrado

@app.post("/tareas")
async def crear_tarea(tarea_data: tarea, session: AsyncSession = Depends(get_session)):
    nueva_tarea = tarea(
        nombre=tarea_data.nombre,
        descripcion=tarea_data.descripcion,
        estado=tarea_data.estado,
        usuario_id=tarea_data.usuario_id,
        creacion=datetime.now(),
        modificacion=None
    )
    session.add(nueva_tarea)
    await session.commit()
    await session.refresh(nueva_tarea)
    return nueva_tarea

@app.get("/tareas")
async def listar_tareas(session: AsyncSession = Depends(get_session)):
    return await obtener_todas_las_tareas(session)

@app.get("/tareas/{tarea_id}")
async def tarea_por_id(tarea_id: int, session: AsyncSession = Depends(get_session)):
    tarea_encontrada = await obtener_tarea_por_id(tarea_id, session)
    if not tarea_encontrada:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return tarea_encontrada

@app.patch("/tareas/{tarea_id}/estado")
async def cambiar_estado_tarea(tarea_id: int, nuevo_estado: EstadoTarea,  session: AsyncSession = Depends(get_session)):
    tarea_actualizada = await actualizar_estado_tarea(tarea_id, nuevo_estado, session)
    if not tarea_actualizada:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return tarea_actualizada
