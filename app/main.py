from fastapi import FastAPI, Request
from app.routes.user_routes import router

app = FastAPI(
    title="device_systems",
    description="API REST para la gestión de usuarios",
    version="1.0"
)


@app.middleware("http")
async def agregar_cabeceras(request: Request, call_next):

    response = await call_next(request)

    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-API-Version"] = "1.0"

    return response


app.include_router(router)