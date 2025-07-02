
from fastapi import FastAPI
from routers import admin_router, veterinaria_router, historial_router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.include_router(admin_router.router, prefix="/admin", tags=["Admin"])


app.include_router(veterinaria_router.router)

# Middleware CORS para permitir peticiones desde la app de escritorio
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Puedes restringir a ["http://localhost"] si prefieres
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "API de Veterinaria funcionando correctamente"}