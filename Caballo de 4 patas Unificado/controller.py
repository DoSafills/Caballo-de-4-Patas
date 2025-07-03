from models import Mascota
from models import Mascota, HistorialMedico
import requests

class MascotaController:
    def __init__(self, db_session, factory):

        self.db = db_session
        self.factory = factory
        self.model_class = Mascota

    def registrar_mascota(self, datos):
        nueva_mascota = self.model_class(**datos)
        self.db.add(nueva_mascota)
        self.db.commit()
        return nueva_mascota

    def buscar_mascota_por_nombre(self, nombre):
        try:
            return self.db.query(self.model_class).filter_by(nombre=nombre).first()
        except Exception as e:
            print(f"[ERROR] al buscar mascota: {e}")
            return None

    def actualizar_mascota(self, id_mascota, nuevos_datos):
        try:
            url = f"http://127.0.0.1:8000/veterinaria/mascotas/{id_mascota}"
            response = requests.put(url, json=nuevos_datos)

            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"No se pudo actualizar: {response.json().get('detail', 'Error desconocido')}")
        except Exception as e:
            print(f"[ERROR] al actualizar mascota vía API: {e}")
            raise

    def obtener_mascota_por_id(self, id_mascota: int):
        try:
            url = f"http://127.0.0.1:8000/veterinaria/mascotas/{id_mascota}"
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"No se pudo obtener información de la mascota: {e}")



    def obtener_historial_por_mascota(self, id_mascota):
        try:
            return self.db.query(HistorialMedico).filter_by(id_mascota=id_mascota).all()
        except Exception as e:
            print(f"[ERROR] al obtener historial: {e}")
            return []

    def agregar_historial(self, id_mascota, descripcion):
        try:
            datos = {
                "descripcion": descripcion,
                "id_mascota": id_mascota
            }
            response = requests.post("http://127.0.0.1:8000/historial/", json=datos)
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(response.json().get("detail", "Error al registrar historial"))
        except Exception as e:
            print(f"[ERROR] al agregar historial vía API: {e}")
            raise

    def listar_mascotas(self):
        try:
            response = requests.get(f"http://127.0.0.1:8000/mascotas/")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error al conectar con la API: {e}")
        
