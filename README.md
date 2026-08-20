# device_systems

Proyecto realizado con **Python y FastAPI** para crear una API REST para la gestión de usuarios.

## Descripción

La aplicación `device_systems` permite consultar usuarios y realizar algunas búsquedas utilizando diferentes parámetros.

Por ahora el proyecto utiliza una lista como base de datos temporal.

## Tecnologías

* Python
* FastAPI
* Uvicorn
* Visual Studio Code

## Estructura del proyecto

```text
device_systems/
│
├── app/
│   ├── main.py
│   ├── schemas/
│   └── routes/
│       └── user_routes.py
│
├── venv/
└── README.md
```

## Instalación

Primero se crea el entorno virtual:

```bash
python -m venv venv
```

Luego se activa en Windows:

```powershell
.\venv\Scripts\activate
```

Después se instalan FastAPI y Uvicorn:

```bash
pip install fastapi uvicorn
```

## Ejecutar el proyecto

Para iniciar el servidor se utiliza:

```bash
uvicorn app.main:app --reload
```

La aplicación queda disponible en:

```text
http://127.0.0.1:8000
```

También se puede acceder a Swagger para probar los endpoints:

```text
http://127.0.0.1:8000/docs
```

## Endpoints realizados

| Método | Endpoint                               | Función                    |
| ------ | -------------------------------------- | -------------------------- |
| GET    | `/users/`                              | Muestra todos los usuarios |
| GET    | `/users/{user_id}`                     | Busca un usuario por su ID |
| GET    | `/users/filtrar/rol?role=admin`        | Filtra usuarios por rol    |
| GET    | `/users/filtrar/estado?is_active=true` | Filtra usuarios por estado |

## Ejemplo de usuario

Los usuarios utilizados actualmente son:

```json
{
    "id": 1,
    "name": "Paula",
    "email": "paula@gmail.com",
    "role": "admin",
    "is_active": true
}
```

Los roles utilizados son:

* `admin`
* `support`
* `user`

## Manejo de errores

También se agregaron algunas validaciones para controlar errores.

Por ejemplo, si se busca un usuario que no existe:

```text
GET /users/50
```

La API responde:

```json
{
    "detail": "Usuario no encontrado"
}
```

También se valida que el ID sea mayor que 0 y que el rol utilizado para los filtros sea válido.

## Estado del proyecto

Hasta el momento se han realizado los endpoints **GET** y sus respectivas validaciones básicas.

## Conclusión

Con este proyecto se están poniendo en práctica los conceptos básicos de **FastAPI y APIs REST**, especialmente el uso de métodos GET, parámetros de ruta, parámetros de consulta y manejo de errores.
