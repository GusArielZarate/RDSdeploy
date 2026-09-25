from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, select
from database import create_db_and_tables, get_session
from models import Usuario, Reserva

app = FastAPI(title="API de Usuarios y Reservas")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

#CRUD USUARIOS 

# 1. Crear registro
@app.post("/usuarios/", response_model=Usuario)
def crear_usuario(usuario: Usuario, session: Session = Depends(get_session)):
    session.add(usuario)
    session.commit()
    session.refresh(usuario)
    return usuario

# 2. Consultar registros
@app.get("/usuarios/", response_model=list[Usuario])
def leer_usuarios(session: Session = Depends(get_session)):
    return session.exec(select(Usuario)).all()

# 3. Consultar un registro específico
@app.get("/usuarios/{usuario_id}", response_model=Usuario)
def leer_usuario_especifico(usuario_id: int, session: Session = Depends(get_session)):
    usuario = session.get(Usuario, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

# 4. Actualizar registro
@app.put("/usuarios/{usuario_id}", response_model=Usuario)
def actualizar_usuario(usuario_id: int, usuario_actualizado: Usuario, session: Session = Depends(get_session)):
    usuario_db = session.get(Usuario, usuario_id)
    if not usuario_db:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    usuario_db.nombre = usuario_actualizado.nombre
    usuario_db.email = usuario_actualizado.email
    
    session.add(usuario_db)
    session.commit()
    session.refresh(usuario_db)
    return usuario_db

# 5. Eliminar registro
@app.delete("/usuarios/{usuario_id}")
def eliminar_usuario(usuario_id: int, session: Session = Depends(get_session)):
    usuario_db = session.get(Usuario, usuario_id)
    if not usuario_db:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    session.delete(usuario_db)
    session.commit()
    return {"mensaje": "Usuario eliminado correctamente"}


#CRUD RESERVAS 

# 1. Crear registro
@app.post("/reservas/", response_model=Reserva)
def crear_reserva(reserva: Reserva, session: Session = Depends(get_session)):
    usuario = session.get(Usuario, reserva.usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="El usuario asignado no existe")
    
    session.add(reserva)
    session.commit()
    session.refresh(reserva)
    return reserva

# 2. Consultar registros
@app.get("/reservas/", response_model=list[Reserva])
def leer_reservas(session: Session = Depends(get_session)):
    return session.exec(select(Reserva)).all()

# 3. Consultar un registro específico
@app.get("/reservas/{reserva_id}", response_model=Reserva)
def leer_reserva_especifica(reserva_id: int, session: Session = Depends(get_session)):
    reserva = session.get(Reserva, reserva_id)
    if not reserva:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    return reserva

# 4. Actualizar registro
@app.put("/reservas/{reserva_id}", response_model=Reserva)
def actualizar_reserva(reserva_id: int, reserva_actualizada: Reserva, session: Session = Depends(get_session)):
    reserva_db = session.get(Reserva, reserva_id)
    if not reserva_db:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    
    # Validar que el nuevo usuario (si se cambia) exista
    if reserva_actualizada.usuario_id:
        usuario = session.get(Usuario, reserva_actualizada.usuario_id)
        if not usuario:
            raise HTTPException(status_code=404, detail="El nuevo usuario asignado no existe")
        reserva_db.usuario_id = reserva_actualizada.usuario_id
        
    reserva_db.descripcion = reserva_actualizada.descripcion
    reserva_db.fecha = reserva_actualizada.fecha
    
    session.add(reserva_db)
    session.commit()
    session.refresh(reserva_db)
    return reserva_db

# 5. Eliminar registro
@app.delete("/reservas/{reserva_id}")
def eliminar_reserva(reserva_id: int, session: Session = Depends(get_session)):
    reserva_db = session.get(Reserva, reserva_id)
    if not reserva_db:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    
    session.delete(reserva_db)
    session.commit()
    return {"mensaje": "Reserva eliminada correctamente"}