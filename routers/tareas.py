from fastapi import APIRouter, HTTPException, Depends
from database import SessionLocal
from models import UsuarioDB, TareaDB
from schemas import Tarea
from auth import obtener_usuario_actual

router = APIRouter(prefix="/tareas", tags=["Tareas"])

@router.post("")
def crear_tarea(tarea: Tarea, email: str = Depends(obtener_usuario_actual)):
    db = SessionLocal()
    usuario = db.query(UsuarioDB).filter(UsuarioDB.email == email).first()
    nueva_tarea = TareaDB(
        titulo=tarea.titulo,
        descripcion=tarea.descripcion,
        usuario_id=usuario.id
    )
    db.add(nueva_tarea)
    db.commit()
    db.refresh(nueva_tarea)
    db.close()
    return {"mensaje": "Tarea creada", "tarea": {
        "id": nueva_tarea.id,
        "titulo": nueva_tarea.titulo,
        "descripcion": nueva_tarea.descripcion,
        "completada": nueva_tarea.completada
    }}

@router.get("")
def ver_tareas(email: str = Depends(obtener_usuario_actual)):
    db = SessionLocal()
    usuario = db.query(UsuarioDB).filter(UsuarioDB.email == email).first()
    tareas = db.query(TareaDB).filter(TareaDB.usuario_id == usuario.id).all()
    db.close()
    return {"tareas": [
        {
            "id": t.id,
            "titulo": t.titulo,
            "descripcion": t.descripcion,
            "completada": t.completada
        } for t in tareas
    ], "total": len(tareas)}

@router.put("/{id}/completar")
def completar_tarea(id: int, email: str = Depends(obtener_usuario_actual)):
    db = SessionLocal()
    usuario = db.query(UsuarioDB).filter(UsuarioDB.email == email).first()
    tarea = db.query(TareaDB).filter(
        TareaDB.id == id,
        TareaDB.usuario_id == usuario.id
    ).first()
    if not tarea:
        db.close()
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    tarea.completada = True
    db.commit()
    db.refresh(tarea)
    db.close()
    return {"mensaje": "Tarea completada ✅"}

@router.delete("/{id}")
def eliminar_tarea(id: int, email: str = Depends(obtener_usuario_actual)):
    db = SessionLocal()
    usuario = db.query(UsuarioDB).filter(UsuarioDB.email == email).first()
    tarea = db.query(TareaDB).filter(
        TareaDB.id == id,
        TareaDB.usuario_id == usuario.id
    ).first()
    if not tarea:
        db.close()
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    db.delete(tarea)
    db.commit()
    db.close()
    return {"mensaje": f"Tarea {id} eliminada exitosamente"}