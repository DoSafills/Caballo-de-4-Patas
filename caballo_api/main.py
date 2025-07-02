from fastapi import FastAPI
# --- Cambiado a import absoluto desde tu paquete caballo_api ---
from caballo_api.routers import admin_router, veterinaria_router, recepcionista_router

app = FastAPI(title="Veterinaria API")

# Admin
app.include_router(
    admin_router.router,
    prefix="/admin",
    tags=["Admin"],
)

# Veterinaria
app.include_router(
    veterinaria_router.router,
    prefix="/veterinaria",
    tags=["Veterinaria"],
)

# Recepcionista
app.include_router(
    recepcionista_router.router,
    prefix="/recepcionista",
    tags=["Recepcionista"],
)
