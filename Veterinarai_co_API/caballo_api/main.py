from fastapi import FastAPI
from routers import admin_router, veterinaria_router, historial_router

app = FastAPI(
    title="API de Veterinaria - Caballo de 4 Patas",
    version="1.0.0"
)

# Routers con etiquetas y prefijos (buenas prácticas)
app.include_router(admin_router.router, prefix="/admin", tags=["Admin"])
app.include_router(veterinaria_router.router, prefix="/veterinaria", tags=["Veterinaria"])
app.include_router(historial_router.router, prefix="/historial", tags=["Historial"])

@app.get("/")
def root():
    return {"message": "API de Veterinaria funcionando correctamente"}

