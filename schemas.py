from pydantic import BaseModel

class UsuarioRegistro(BaseModel):
    nombre: str
    email: str
    password: str

class Tarea(BaseModel):
    titulo: str
    descripcion: str