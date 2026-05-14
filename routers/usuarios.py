from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from database import SessionLocal
from models import UsuarioDB
from schemas import UsuarioRegistro
from auth import encriptar_password, verificar_password, crear_token

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

@router.post("/registro")
def registrar(usuario: UsuarioRegistro):
    db = SessionLocal()
    existe = db.query(UsuarioDB).filter(UsuarioDB.email == usuario.email).first()
    if existe:
        db.close()
        raise HTTPException(status_code=400, detail="Email ya registrado")
    nuevo = UsuarioDB(
        nombre=usuario.nombre,
        email=usuario.email,
        password=encriptar_password(usuario.password)
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    db.close()
    return {"mensaje": f"Usuario {usuario.nombre} registrado exitosamente"}

@router.post("/login")
def login(form: OAuth2PasswordRequestForm = Depends()):
    db = SessionLocal()
    usuario = db.query(UsuarioDB).filter(UsuarioDB.email == form.username).first()
    db.close()
    if not usuario or not verificar_password(form.password, usuario.password):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    token = crear_token({"sub": usuario.email})
    return {"access_token": token, "token_type": "bearer"}