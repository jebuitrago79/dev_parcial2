'''Aqui debes consignar el modelo que se te indico en el parcial
Escribe aquí el que te corresponde.

'''
from sqlmodel import SQLModel, Field
from typing import Optional
from enum import Enum

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
