import customtkinter as ctk
from tkinter import messagebox
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import crud
import models
from models import create_tables
import os
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "veterinaria.db")
engine = create_engine(f"sqlite:///{DB_PATH}")
Session = sessionmaker(bind=engine)
db = Session()
# Justo antes de crear la app
create_tables(engine)


class VeterinariaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Registro de Mascotas")
        self.root.geometry("600x1050")
        self.root.resizable(False, False)

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

        ctk.CTkLabel(self.root, text="Registro de Mascota", font=("Arial", 22, "bold")).pack(pady=15)

        form_frame = ctk.CTkFrame(self.root)
        form_frame.pack(pady=20, fill="x", padx=30)

        campos = [
            ("Nombre", self.nombre_mascota, "Firulais"),
            ("Raza", self.raza, "Golden Retriever"),
            ("Sexo", self.sexo, "Macho/Hembra"),
            ("Dieta", self.dieta, "Normal/Especial"),
            ("Carácter", self.caracter, "Tranquilo, etc."),
            ("Hábitat", self.habitat, "Casa, Patio..."),
            ("Edad", self.edad, "Ej: 3"),
            ("Peso (kg)", self.peso, "Ej: 10.5"),
            ("Altura (cm)", self.altura, "Ej: 40")
        ]

        for texto, var, placeholder in campos:
            ctk.CTkLabel(form_frame, text=texto).pack(anchor="w")
            ctk.CTkEntry(form_frame, textvariable=var, placeholder_text=placeholder).pack(fill="x", pady=3)

        # ComboBox de veterinarios
        veterinarios = db.query(models.Veterinario).all()
        self.vet_ids = [f"{vet.id_vet} - {vet.nombre}" for vet in veterinarios]

        ctk.CTkLabel(form_frame, text="Veterinario").pack(anchor="w")
        ctk.CTkComboBox(form_frame, values=self.vet_ids, variable=self.vet_seleccionado).pack(fill="x", pady=3)

        boton_frame = ctk.CTkFrame(self.root, fg_color="white")
        boton_frame.pack(pady=20)

        ctk.CTkButton(boton_frame, text="REGISTRAR", fg_color="#007BFF", text_color="white",
                    width=120, command=self.registrar_mascota).pack(side="left", padx=10)

        ctk.CTkButton(boton_frame, text="SALIR", fg_color="black", text_color="white", width=120,
                    command=self.root.destroy).pack(side="left", padx=10)

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

            mascota_data = {
                "nombre": self.nombre_mascota.get(),
                "raza": self.raza.get(),
                "sexo": self.sexo.get(),
                "dieta": self.dieta.get(),
                "caracter": self.caracter.get(),
                "habitat": self.habitat.get(),
                "edad": int(self.edad.get()),
                "peso": self.peso.get(),
                "altura": self.altura.get(),
                "id_vet": id_vet
            }
            mascota = crud.crear_mascota(db, mascota_data)
            messagebox.showinfo("Éxito", f"Mascota '{mascota.nombre}' registrada correctamente.")

            for var in [self.nombre_mascota, self.raza, self.sexo, self.dieta,
                        self.caracter, self.habitat, self.edad, self.peso, self.altura, self.vet_seleccionado]:
                var.set("")

        except Exception as e:
            db.rollback()
            messagebox.showerror("Error", str(e))

if __name__ == '__main__':
    root = ctk.CTk()
    app = VeterinariaApp(root)
    root.mainloop()
