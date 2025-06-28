from models import Mascota
from models import Mascota, HistorialMedico

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
            mascota = self.db.query(self.model_class).get(id_mascota)
            if mascota is None:
                raise Exception("Mascota no encontrada")

            for clave, valor in nuevos_datos.items():
                setattr(mascota, clave, valor)

            self.db.commit()
            return mascota

        except Exception as e:
            self.db.rollback()
            print(f"[ERROR] al actualizar mascota: {e}")
            raise e

    def obtener_historial_por_mascota(self, id_mascota):
        try:
            return self.db.query(HistorialMedico).filter_by(id_mascota=id_mascota).all()
        except Exception as e:
            print(f"[ERROR] al obtener historial: {e}")
            return []

    def agregar_historial(self, id_mascota, descripcion):
        try:
            nuevo = HistorialMedico(
                id_mascota=id_mascota,
                descripcion=descripcion
            )
            self.db.add(nuevo)
            self.db.commit()
            return nuevo
        except Exception as e:
            self.db.rollback()
            print(f"[ERROR] al agregar historial: {e}")
            raise e

    def obtener_historial(self, id_mascota):
        return self.obtener_historial_por_mascota(id_mascota)
