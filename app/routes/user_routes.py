from fastapi import APIRouter, HTTPException, Query
from app.schemas.user_schema import UserCreate, UserResponse, UserUpdate

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

# Base de datos temporal
base_datos = [
    {
        "id": 1,
        "name": "Paula",
        "email": "paula@gmail.com",
        "role": "admin",
        "is_active": True
    },
    {
        "id": 2,
        "name": "Carlos",
        "email": "carlos@gmail.com",
        "role": "support",
        "is_active": True
    },
    {
        "id": 3,
        "name": "Ana",
        "email": "ana@gmail.com",
        "role": "admin",
        "is_active": False
    },
    {
        "id": 4,
        "name": "Cristian",
        "email": "cristian@gmail.com",
        "role": "admin",
        "is_active": False
    }
]


@router.get("/", response_model=list[UserResponse])
def obtener_usuarios(
    role: str | None = Query(default=None),
    is_active: bool | None = Query(default=None)
):

    usuarios = base_datos

    if role is not None:
        usuarios = [
            usuario for usuario in usuarios
            if usuario["role"] == role
        ]

    if is_active is not None:
        usuarios = [
            usuario for usuario in usuarios
            if usuario["is_active"] == is_active
        ]

    if not usuarios:
        raise HTTPException(
            status_code=404,
            detail="No se encontraron usuarios"
        )

    return usuarios

@router.get("/{id}", response_model=UserResponse)
def obtener_usuario(id: int):
    for usuario in base_datos:
        if usuario["id"] == id:
            return usuario

    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )


@router.post("/", response_model=UserResponse, status_code=201)
def crear_usuario(usuario: UserCreate):

    for usuario_existente in base_datos:
        if usuario_existente["email"] == usuario.email:
            raise HTTPException(
                status_code=400,
                detail="El correo electrónico ya está registrado"
            )

    nuevo_id = max([usuario["id"] for usuario in base_datos], default=0) + 1

    nuevo_usuario = {
        "id": nuevo_id,
        "name": usuario.name,
        "email": usuario.email,
        "role": usuario.role,
        "is_active": usuario.is_active
    }

    base_datos.append(nuevo_usuario)

    return nuevo_usuario


@router.put("/{id}", response_model=UserResponse)
def actualizar_usuario(id: int, usuario: UserCreate):
    for usuario_existente in base_datos:
        if usuario_existente["id"] == id:
            usuario_existente["name"] = usuario.name
            usuario_existente["email"] = usuario.email
            usuario_existente["role"] = usuario.role
            usuario_existente["is_active"] = usuario.is_active

            return usuario_existente

    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )


@router.patch("/{id}", response_model=UserResponse)
def actualizar_usuario_parcial(id: int, usuario: UserUpdate):
    for usuario_existente in base_datos:
        if usuario_existente["id"] == id:

            if usuario.name is not None:
                usuario_existente["name"] = usuario.name

            if usuario.email is not None:
                usuario_existente["email"] = usuario.email

            if usuario.role is not None:
                usuario_existente["role"] = usuario.role

            if usuario.is_active is not None:
                usuario_existente["is_active"] = usuario.is_active

            return usuario_existente

    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )


@router.delete("/{id}")
def eliminar_usuario(id: int):
    for usuario in base_datos:
        if usuario["id"] == id:
            base_datos.remove(usuario)

            return {
                "message": "Usuario eliminado correctamente"
            }

    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )