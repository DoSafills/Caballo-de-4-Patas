import customtkinter as ctk
from tkinter import messagebox
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import crud
import models
from models import create_tables
import os
from controller import MascotaController  # <-- Controlador

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
        self.root.geometry("600x1050")
        self.root.resizable(False, False)
        self.root.configure(bg="#f0f0f0")

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
        self.vet_seleccionado = ctk.StringVar()

        ctk.CTkLabel(self.root, text="Registro de Mascota", font=("Arial", 22, "bold"), text_color="#333").pack(pady=15)

        form_frame = ctk.CTkFrame(self.root, corner_radius=0, border_width=1, border_color="#cccccc")
        form_frame.pack(pady=20, fill="x", padx=30)

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

        ctk.CTkButton(boton_frame, text="REGISTRAR", fg_color="#2c3e50", text_color="white",
                    width=120, command=self.registrar_mascota, corner_radius=0).pack(side="left", padx=10)

        ctk.CTkButton(boton_frame, text="SALIR", fg_color="#7f8c8d", text_color="white", width=120,
                    command=self.root.destroy, corner_radius=0).pack(side="left", padx=10)

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
