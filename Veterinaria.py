import customtkinter as ctk
from tkinter import messagebox
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import models
from models import create_tables
import os
from controller import MascotaController  # <-- Controlador
from factories import VentanaFactory


#  FACTORY
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
            "altura": altura,
            "id_vet": id_vet
        }

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# Ruta al directorio actual
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
db_path = os.path.join(parent_dir, "veterinaria.db")
engine = create_engine(f"sqlite:///{db_path}")
Session = sessionmaker(bind=engine)
db = Session()
create_tables(engine)

class VeterinariaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Registro de Mascotas")
        self.root.geometry("1024x768")
        self.root.configure(bg="#f7f7f7")
        self.controller = MascotaController(db, MascotaFactory)

        # Variables
        self.nombre_mascota = ctk.StringVar()
        self.raza = ctk.StringVar()
        self.sexo = ctk.StringVar()
        self.dieta = ctk.StringVar()
        self.caracter = ctk.StringVar()
        self.habitat = ctk.StringVar()
        self.edad = ctk.StringVar()
        self.peso = ctk.StringVar()
        self.altura = ctk.StringVar()
        self.vacunas = ctk.BooleanVar()
        self.vet_seleccionado = ctk.StringVar()


        self.nombre_duenio = ctk.StringVar()
        self.email_duenio = ctk.StringVar()
        self.telefono_duenio = ctk.StringVar()


        self.main_card()

    def main_card(self):
        container = ctk.CTkFrame(self.root, fg_color="#ffffff", corner_radius=20)
        container.pack(pady=40, padx=40, fill="both")

        ctk.CTkLabel(container, text="HOME PETS", font=("Arial", 20, "bold"), text_color="#000").pack(anchor="nw", pady=(15, 0), padx=20)
        ctk.CTkLabel(container, text="Asistencia de Reserva", font=("Arial", 22, "bold"), text_color="#000").pack(pady=(0, 5))
        ctk.CTkLabel(container, text="Precio de la consulta: S/. 50.00", font=("Arial", 14), text_color="#555").pack(pady=(0, 20))

        
        # Marco principal dividido en navegación y contenido
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True)


        


        nav_frame = ctk.CTkFrame(main_frame, width=200)
        nav_frame.pack(side="left", fill="y", padx=10, pady=10)

        form_frame = ctk.CTkFrame(container, fg_color="#ffffff")
        form_frame.pack(padx=30, pady=20, fill="both")

        form_frame.grid_columnconfigure(0, weight=1)
        form_frame.grid_columnconfigure(1, weight=1)


    # Entradas tipo texto
        campos = [
            ("Nombre", self.nombre_mascota, "Firulais"),
            ("Raza", self.raza, "Golden Retriever"),
            ("Edad", self.edad, "Ej: 3"),
            ("Peso (kg)", self.peso, "Ej: 10.5"),
            ("Altura (cm)", self.altura, "Ej: 40")
        ]

        for texto, var, placeholder in campos:
            ctk.CTkLabel(form_frame, text=texto, text_color="#555").pack(anchor="w")
            ctk.CTkEntry(form_frame, textvariable=var, placeholder_text=placeholder, corner_radius=0).pack(fill="x", pady=4)

        # ComboBoxes predefinidos
        ctk.CTkLabel(form_frame, text="Sexo", text_color="#555").pack(anchor="w")
        ctk.CTkComboBox(form_frame, values=["Macho", "Hembra"], variable=self.sexo, state="readonly", corner_radius=0).pack(fill="x", pady=4)

        ctk.CTkLabel(form_frame, text="Dieta", text_color="#555").pack(anchor="w")
        ctk.CTkComboBox(form_frame, values=["Normal", "Especial", "Dietética"], variable=self.dieta, state="readonly", corner_radius=0).pack(fill="x", pady=4)

        ctk.CTkLabel(form_frame, text="Carácter", text_color="#555").pack(anchor="w")
        ctk.CTkComboBox(form_frame, values=["Tranquilo", "Agresivo", "Juguetón", "Tímido"], variable=self.caracter, state="readonly", corner_radius=0).pack(fill="x", pady=4)

        ctk.CTkLabel(form_frame, text="Hábitat", text_color="#555").pack(anchor="w")
        ctk.CTkComboBox(form_frame, values=["Casa", "Patio", "Campo", "Interior", "Exterior"], variable=self.habitat, state="readonly", corner_radius=0).pack(fill="x", pady=4)

        # Veterinarios
        veterinarios = db.query(models.Veterinario).all()
        self.vet_ids = [f"{vet.id_vet} - {vet.nombre}" for vet in veterinarios]

        ctk.CTkLabel(form_frame, text="Veterinario", text_color="#555").pack(anchor="w")
        ctk.CTkComboBox(form_frame, values=self.vet_ids, variable=self.vet_seleccionado, state="readonly", corner_radius=0).pack(fill="x", pady=4)

        # Botones
        boton_frame = ctk.CTkFrame(self.root, fg_color="#ffffff", corner_radius=0, border_width=1, border_color="#cccccc")
        boton_frame.pack(pady=20)

        ctk.CTkLabel(nav_frame, text="Menú", font=("Arial", 16, "bold")).pack(pady=10)
        ctk.CTkButton(boton_frame, text="REGISTRAR", fg_color="#2c3e50", text_color="white",
                    width=120, command=self.registrar_mascota, corner_radius=0).pack(side="left", padx=10)
        ctk.CTkButton(nav_frame, text="Gestionar Mascotas", command=self.abrir_gestion_ventana, fg_color="#2980b9", text_color="white").pack(pady=5, fill="x")
        ctk.CTkButton(nav_frame, text="Historial Médico", command=self.abrir_historial_ventana, fg_color="#8e44ad", text_color="white").pack(pady=5, fill="x")

        ctk.CTkButton(nav_frame, text="Salir", command=self.root.quit, fg_color="#c0392b", text_color="white").pack(pady=5, fill="x")
# factory


    def abrir_historial_ventana(self):
        from factories import VentanaFactory
        VentanaFactory.crear("historial", self.root, self.controller)


    def abrir_gestion_ventana(self):
        VentanaFactory.crear("gestion", self.root, self.controller)


    def registrar_mascota(self):
        campos = [
            self.nombre_mascota.get(), self.raza.get(), self.sexo.get(), self.dieta.get(),
            self.caracter.get(), self.habitat.get(), self.edad.get(),
            self.peso.get(), self.altura.get(), self.vet_seleccionado.get()
        ]
        if not all(campos):
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        try:
            id_vet = int(self.vet_seleccionado.get().split(" - ")[0])

            datos = {
                "nombre": self.nombre_mascota.get(),
                "raza": self.raza.get(),
                "sexo": self.sexo.get(),
                "dieta": self.dieta.get(),
                "caracter": self.caracter.get(),
                "habitat": self.habitat.get(),
                "edad": self.edad.get(),
                "peso": self.peso.get(),
                "altura": self.altura.get(),
                "id_vet": id_vet
            }

            mascota = self.controller.registrar_mascota(datos)
            messagebox.showinfo("Éxito", f"Mascota '{mascota.nombre}' registrada correctamente.")

            for var in [self.nombre_mascota, self.raza, self.sexo, self.dieta,
                        self.caracter, self.habitat, self.edad, self.peso, self.altura, self.vet_seleccionado]:
                var.set("")

        except Exception as e:
            db.rollback()
            messagebox.showerror("Error", str(e))


    def cerrar(self):
        self.db.cloce()

if __name__ == "__main__":
    root = ctk.CTk()
    app = VeterinariaApp(root)
    root.protocol('WM_DELTE_WINDOW')
    root.mainloop()
