from fastapi import APIRouter, HTTPException

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


# GET /users/
@router.get("/")
def obtener_usuarios():

    if not base_datos:
        raise HTTPException(
            status_code=404,
            detail="No hay usuarios registrados"
        )

    return base_datos


# GET /users/filtrar/rol
@router.get("/filtrar/rol")
def filtrar_por_rol(role: str):

    # Validar que se haya enviado el rol
    if not role:
        raise HTTPException(
            status_code=400,
            detail="Debe proporcionar un rol"
        )

    # Validar roles permitidos
    roles_permitidos = ["admin", "support", "user"]

    if role not in roles_permitidos:
        raise HTTPException(
            status_code=400,
            detail="Rol no válido. Los roles permitidos son: admin, support, user"
        )

    usuarios = []

    for usuario in base_datos:
        if usuario["role"] == role:
            usuarios.append(usuario)

    # Si no hay usuarios con ese rol
    if not usuarios:
        raise HTTPException(
            status_code=404,
            detail="No se encontraron usuarios con ese rol"
        )

    return usuarios


# GET /users/filtrar/estado
@router.get("/filtrar/estado")
def filtrar_por_estado(is_active: bool):

    usuarios = []

    for usuario in base_datos:
        if usuario["is_active"] == is_active:
            usuarios.append(usuario)

    # Si no existen usuarios con ese estado
    if not usuarios:
        raise HTTPException(
            status_code=404,
            detail="No se encontraron usuarios con ese estado"
        )

    return usuarios


# GET /users/{user_id}
@router.get("/{user_id}")
def obtener_usuario(user_id: int):

    # Validar que el ID sea positivo
    if user_id <= 0:
        raise HTTPException(
            status_code=400,
            detail="El ID debe ser un número mayor que 0"
        )

    # Buscar usuario por ID
    for usuario in base_datos:
        if usuario["id"] == user_id:
            return usuario

    # Si no encuentra el usuario
    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )