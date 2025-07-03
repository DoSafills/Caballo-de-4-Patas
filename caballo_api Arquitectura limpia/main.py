
from fastapi import FastAPI
from routers import admin_router, veterinaria_router, recepcionista_router, historial_router, login_router

app = FastAPI()

app.include_router(admin_router.router, prefix="/admin", tags=["Admin"])


app.include_router(veterinaria_router.router)

app.include_router(recepcionista_router.router)

app.include_router(veterinaria_router.router, prefix="/veterinaria", tags=["Veterinaria"])

app.include_router(historial_router.router, prefix="/historial", tags=["Historial"])
app.include_router(login_router.router, prefix="/auth", tags=["Autenticación"])

@app.get("/")
def root():
    return {"message": "API de Veterinaria funcionando correctamente"}