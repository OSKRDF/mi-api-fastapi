from fastapi import FastAPI
from database import Base, engine
from routers import usuarios, tareas

# Crear tablas
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Mi API", version="1.0")

# Registrar routers
app.include_router(usuarios.router)
app.include_router(tareas.router)

@app.get("/")
def inicio():
    return {"mensaje": "API funcionando ✅"}