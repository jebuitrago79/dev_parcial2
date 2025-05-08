'''Aqui debes construir las operaciones que se te han indicado'''
from sqlmodel import Session, select
from data.models import usuario, tarea, EstadoTarea
from sqlmodel.ext.asyncio.session import AsyncSession
from datetime import datetime

async def actualizar_usuario(usuario_id: int, datos: dict, session: AsyncSession):
    usuario_db = await session.get(usuario, usuario_id)
    if usuario_db:
        for key, value in datos.items():
            setattr(usuario_db, key, value)
        await session.commit()
        await session.refresh(usuario_db)
    return usuario_db

async def hacer_usuario_premium(usuario_id: int, session: AsyncSession):
    usuario_db = await session.get(usuario, usuario_id)
    if not usuario_db:
        return None
    usuario_db.premium = True
    await session.commit()
    await session.refresh(usuario_db)
    return usuario_db


async def obtener_usuarios_activos(session: AsyncSession):
    consulta = select(usuario).where(usuario.estado == "activo")
    resultado = await session.exec(consulta)
    return resultado.all()

async def obtener_usuarios_premium_activos(session: AsyncSession):
    consulta = select(usuario).where(
        usuario.estado == "activo",
        usuario.premium == True
    )
    resultado = await session.exec(consulta)
    return resultado.all()

async def crear_tarea(nueva_tarea: tarea, session: AsyncSession):
    session.add(nueva_tarea)
    await session.commit()
    await session.refresh(nueva_tarea)
    return nueva_tarea

async def obtener_todas_las_tareas(session: AsyncSession):
    query = select(tarea)
    result = await session.exec(query)
    return result.all()

async def obtener_tarea_por_id (tarea_id: int, session: AsyncSession):
    query = select(tarea).where(tarea.id == tarea_id)
    result = await session.exec(query)
    return result.first()


async def actualizar_estado_tarea(tarea_id: int, nuevo_estado: EstadoTarea, session: AsyncSession):
    result = await session.exec(select(tarea).where(tarea.id == tarea_id))
    tarea_encontrada = result.first()

    if not tarea_encontrada:
        return None

    tarea_encontrada.estado = nuevo_estado
    tarea_encontrada.modificacion = datetime.utcnow()

    session.add(tarea_encontrada)
    await session.commit()
    await session.refresh(tarea_encontrada)

    return tarea_encontrada

async def obtener_tareas_por_usuario(usuario_id: int, session: AsyncSession):
    query = select(tarea).where(tarea.usuario_id == usuario_id)
    result = await session.exec(query)
    return result.all()
