from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship

class Usuario(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    email: str

    reservas: List["Reserva"] = Relationship(back_populates="usuario")

class Reserva(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    descripcion: str
    fecha: str
    usuario_id: Optional[int] = Field(default=None, foreign_key="usuario.id")
    usuario: Optional[Usuario] = Relationship(back_populates="reservas")