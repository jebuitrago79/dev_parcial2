'''Aqui debes construir las operaciones que se te han indicado'''
from sqlmodel import Session, select
from data.models import usuario
from utils.connection_db import get_session
from sqlmodel.ext.asyncio.session import AsyncSession

async def actualizar_usuario(usuario_id: int, datos: dict, session: AsyncSession):
    usuario_db = await session.get(usuario, usuario_id)
    if usuario_db:
        for key, value in datos.items():
            setattr(usuario_db, key, value)
        await session.commit()
        await session.refresh(usuario_db)
    return usuario_db



