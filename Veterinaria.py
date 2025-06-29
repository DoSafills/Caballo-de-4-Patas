import customtkinter as ctk
from tkinter import messagebox
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import Veterinaria.models as models
from Veterinaria.models import create_tables
import os
from controller import MascotaController
from factories import VentanaFactory

# FACTORY
class MascotaFactory:
    @staticmethod
    def crear(nombre, raza, sexo, dieta, caracter, habitat, edad, peso, altura, id_vet):
        return {
            "nombre": nombre,
            "raza": raza,
            "sexo": sexo,
            "dieta": dieta,
            "caracter": caracter,
            "habitat": habitat,
            "edad": int(edad),
            "peso": peso,
            "altura": altura
           
        }

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

current_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(current_dir, "veterinaria.db")

engine = create_engine(f"sqlite:///{db_path}")
Session = sessionmaker(bind=engine)
db = Session()

class VeterinariaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Asistencia de Reserva")
        self.root.geometry("950x720")
        self.root.configure(bg="#f7f7f7")

        self.controller = MascotaController(db, MascotaFactory)

        self.nombre_mascota = ctk.StringVar()
        self.raza = ctk.StringVar()
        self.sexo = ctk.StringVar()
        self.edad = ctk.StringVar()
        self.dieta = ctk.StringVar()
        self.caracter = ctk.StringVar()
        self.habitat = ctk.StringVar()
        self.peso = ctk.StringVar()
        self.altura = ctk.StringVar()

        self.main_card()

    def main_card(self):
        container = ctk.CTkFrame(self.root, fg_color="#ffffff", corner_radius=20)
        container.pack(pady=20, padx=20, fill="both", expand=True)

        ctk.CTkLabel(container, text="HOME PETS", font=("Arial", 20, "bold"), text_color="#000").pack(anchor="nw", pady=(15, 0), padx=20)
        ctk.CTkLabel(container, text="Asistencia de Reserva", font=("Arial", 22, "bold"), text_color="#000").pack(pady=(0, 5))
        ctk.CTkLabel(container, text="Precio de la consulta: CLP: 5.000", font=("Arial", 14), text_color="#555").pack(pady=(0, 20))

        progress_frame = ctk.CTkFrame(container, fg_color="#ffffff")
        progress_frame.pack(pady=10)
        steps = ["ESPECIALIDAD", "PROFESIONAL", "FECHA Y HORA", "AQUI -----> DATOS"]
        for i, step in enumerate(steps):
            ctk.CTkLabel(progress_frame, text="●", text_color="#f57c00", font=("Arial", 18)).pack(side="left")
            ctk.CTkLabel(progress_frame, text=step, text_color="#000", font=("Arial", 12, "bold"), padx=10).pack(side="left")
            if i < len(steps) - 1:
                ctk.CTkLabel(progress_frame, text="▬" * 5, text_color="#f57c00").pack(side="left")

        form_frame = ctk.CTkFrame(container, fg_color="#ffffff")
        form_frame.pack(padx=30, pady=20, fill="both", expand=True)
        form_frame.grid_columnconfigure(0, weight=1)
        form_frame.grid_columnconfigure(1, weight=1)

        izquierda = ctk.CTkFrame(form_frame, fg_color="#ffffff")
        izquierda.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        derecha = ctk.CTkFrame(form_frame, fg_color="#ffffff")
        derecha.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        ctk.CTkLabel(izquierda, text="Datos de la Mascota", font=("Arial", 16, "bold"), text_color="#000").pack(anchor="w", pady=(0, 10))

        for label, var, placeholder in [
            ("Nombre:", self.nombre_mascota, "Fido"),
            ("Raza:", self.raza, "Golden"),
            ("Peso (kg):", self.peso, "10.5"),
            ("Altura (cm):", self.altura, "40")
        ]:
            row = ctk.CTkFrame(izquierda, fg_color="#ffffff")
            row.pack(fill="x", pady=4)
            ctk.CTkLabel(row, text=label, text_color="#666", width=120).pack(side="left")
            ctk.CTkEntry(row, textvariable=var, placeholder_text=placeholder, width=160).pack(side="left", padx=10)

        row3 = ctk.CTkFrame(izquierda, fg_color="#ffffff")
        row3.pack(fill="x", pady=4)
        ctk.CTkLabel(row3, text="Sexo:", text_color="#666", width=120).pack(side="left")
        sexo_frame = ctk.CTkFrame(row3, fg_color="#ffffff")
        sexo_frame.pack(side="left")
        ctk.CTkRadioButton(sexo_frame, text="Macho", value="Macho", variable=self.sexo).pack(side="left", padx=5)
        ctk.CTkRadioButton(sexo_frame, text="Hembra", value="Hembra", variable=self.sexo).pack(side="left", padx=5)

        row4 = ctk.CTkFrame(izquierda, fg_color="#ffffff")
        row4.pack(fill="x", pady=4)
        ctk.CTkLabel(row4, text="Edad:", text_color="#666", width=120).pack(side="left")
        ctk.CTkComboBox(row4, values=[f"{i} años" for i in range(1, 21)], variable=self.edad, width=160).pack(side="left", padx=10)

        for label, var, options in [
            ("Dieta:", self.dieta, ["Normal", "Especial", "Dietética"]),
            ("Carácter:", self.caracter, ["Tranquilo", "Agresivo", "Juguetón", "Tímido"]),
            ("Hábitat:", self.habitat, ["Casa", "Patio", "Campo", "Interior", "Exterior"])
        ]:
            row = ctk.CTkFrame(derecha, fg_color="#ffffff")
            row.pack(fill="x", pady=4)
            ctk.CTkLabel(row, text=label, text_color="#666", width=120).pack(side="left")
            ctk.CTkComboBox(row, values=options, variable=var, width=160).pack(side="left", padx=10)

        botones = ctk.CTkFrame(container, fg_color="#ffffff")
        botones.pack(pady=10, padx=20, fill="x")
        ctk.CTkButton(botones, text="SALIR", command=self.root.quit, fg_color="#ffffff", text_color="#000", border_width=1, border_color="#000", width=120).pack(side="left", padx=10)
        ctk.CTkButton(botones, text="GESTIÓN", command=self.abrir_gestion_ventana, fg_color="#3498db", text_color="#fff", width=120).pack(side="left", padx=10)
        ctk.CTkButton(botones, text="HISTORIAL", command=self.abrir_historial_ventana, fg_color="#8e44ad", text_color="#fff", width=120).pack(side="left", padx=10)
        ctk.CTkButton(botones, text="REGISTRAR", command=self.registrar_mascota, fg_color="#f57c00", text_color="#fff", hover_color="#e65100", width=120).pack(side="right", padx=10)

    def abrir_gestion_ventana(self):
        VentanaFactory.crear("gestion", self.root, self.controller)

    def abrir_historial_ventana(self):
        VentanaFactory.crear("historial", self.root, self.controller)

    def registrar_mascota(self):
        if not all([
            self.nombre_mascota.get(), self.raza.get(), self.sexo.get(), self.edad.get(),
            self.dieta.get(), self.caracter.get(), self.habitat.get(), self.peso.get(), self.altura.get()
        ]):
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        try:
            datos = {
                "nombre": self.nombre_mascota.get(),
                "raza": self.raza.get(),
                "sexo": self.sexo.get(),
                "dieta": self.dieta.get(),
                "caracter": self.caracter.get(),
                "habitat": self.habitat.get(),
                "edad": self.edad.get().split()[0],
                "peso": self.peso.get(),
                "altura": self.altura.get()
           
            }
            mascota = self.controller.registrar_mascota(datos)
            messagebox.showinfo("Éxito", f"Mascota '{mascota.nombre}' registrada correctamente.")

            for var in [self.nombre_mascota, self.raza, self.sexo, self.edad, self.dieta, self.caracter, self.habitat, self.peso, self.altura]:
                var.set("")

        except Exception as e:
            db.rollback()
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = ctk.CTk()
    app = VeterinariaApp(root)
    root.mainloop()
