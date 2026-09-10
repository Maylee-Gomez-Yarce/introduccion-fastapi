from fastapi import APIRouter, HTTPException, Query, Depends

from app.schemas.user_schema import UserCreate, UserResponse, UserUpdate
from app.database import SessionLocal
from app.models.usuario import Usuario

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=list[UserResponse])
def obtener_usuarios(
    role: str | None = Query(default=None),
    is_active: bool | None = Query(default=None),
    db=Depends(get_db)
):
    consulta = db.query(Usuario)

    if role is not None:
        consulta = consulta.filter(Usuario.role == role)

    if is_active is not None:
        consulta = consulta.filter(Usuario.is_active == is_active)

    usuarios = consulta.all()

    if not usuarios:
        raise HTTPException(
            status_code=404,
            detail="No se encontraron usuarios"
        )

    return usuarios


@router.get("/{id}", response_model=UserResponse)
def obtener_usuario(
    id: int,
    db=Depends(get_db)
):
    usuario = db.query(Usuario).filter(Usuario.id == id).first()

    if usuario is None:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    return usuario


@router.post("/", response_model=UserResponse, status_code=201)
def crear_usuario(
    usuario: UserCreate,
    db=Depends(get_db)
):
    usuario_existente = db.query(Usuario).filter(
        Usuario.email == usuario.email
    ).first()

    if usuario_existente:
        raise HTTPException(
            status_code=400,
            detail="El correo electrónico ya está registrado"
        )

    nuevo_usuario = Usuario(
        name=usuario.name,
        email=usuario.email,
        role=usuario.role,
        is_active=usuario.is_active
    )

    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)

    return nuevo_usuario


@router.put("/{id}", response_model=UserResponse)
def actualizar_usuario(
    id: int,
    usuario: UserCreate,
    db=Depends(get_db)
):
    usuario_existente = db.query(Usuario).filter(
        Usuario.id == id
    ).first()

    if usuario_existente is None:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    usuario_existente.name = usuario.name
    usuario_existente.email = usuario.email
    usuario_existente.role = usuario.role
    usuario_existente.is_active = usuario.is_active

    db.commit()
    db.refresh(usuario_existente)

    return usuario_existente


@router.patch("/{id}", response_model=UserResponse)
def actualizar_usuario_parcial(
    id: int,
    usuario: UserUpdate,
    db=Depends(get_db)
):
    usuario_existente = db.query(Usuario).filter(
        Usuario.id == id
    ).first()

    if usuario_existente is None:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    if usuario.name is not None:
        usuario_existente.name = usuario.name

    if usuario.email is not None:
        usuario_existente.email = usuario.email

    if usuario.role is not None:
        usuario_existente.role = usuario.role

    if usuario.is_active is not None:
        usuario_existente.is_active = usuario.is_active

    db.commit()
    db.refresh(usuario_existente)

    return usuario_existente


@router.delete("/{id}")
def eliminar_usuario(
    id: int,
    db=Depends(get_db)
):
    usuario = db.query(Usuario).filter(
        Usuario.id == id
    ).first()

    if usuario is None:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    db.delete(usuario)
    db.commit()

    return {
        "message": "Usuario eliminado correctamente"
    }