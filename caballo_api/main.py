
from fastapi import FastAPI
from routers import admin_router, veterinaria_router

app = FastAPI()

app.include_router(admin_router.router, prefix="/admin", tags=["Admin"])


app.include_router(veterinaria_router.router)
