'''Aqui debes consignar el modelo que se te indico en el parcial
Escribe aquí el que te corresponde.

'''
from sqlmodel import SQLModel, Field
from typing import Optional
from enum import Enum
from datetime import datetime

class EstadoTarea(str, Enum):
    pendiente = "Pendiente"
    en_ejecucion = "En ejecucion"
    realizado = "Realizado"
    cancelada = "Cancelada"

class estado_Usuario (str, Enum):
    activo= "activo"
    inactivo = "inactivo"
    eliminado = "eliminado"


class usuario (SQLModel, table= True):
    __tablename__ = "usuarios"
    id : Optional[int]=Field(default=None, primary_key=True)
    nombre : str
    email : str
    estado : estado_Usuario = Field(default=estado_Usuario.activo)
    premium : bool = False

class tarea (SQLModel, table= True):
    __tablename__ = "Tareas"
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    descripcion : str
    creacion: Optional[datetime] = Field(default_factory=datetime.now)
    modificacion: Optional[datetime] = Field(default=None)
    estado: EstadoTarea = Field(default=EstadoTarea.pendiente)
    usuario_id: int = Field(foreign_key="usuarios.id")