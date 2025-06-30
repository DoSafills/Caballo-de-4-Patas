from database import get_session
from models import Admin, Recepcionista, Veterinario

def authenticate(rut: str, password: str):
    with get_session() as db:
        for model, tipo in [(Admin, "admin"), (Recepcionista, "recepcionista"), (Veterinario, "veterinario")]:
            user = db.query(model).filter_by(rut=rut).first()
            if user and user.contrasena == password:
                return user, tipo
        return None, None
