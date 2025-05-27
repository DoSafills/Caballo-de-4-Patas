import customtkinter as ctk
from tkinter import messagebox
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import crud
import models

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# Configurar la base de datos
engine = create_engine("sqlite:///veterinaria.db")
Session = sessionmaker(bind=engine)
db = Session()

class VeterinariaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Registro de Mascotas")
        self.root.geometry("750x600")
        self.root.resizable(False, False)

        # -------------- VARIABLES ----------------
        self.nombre_mascota = ctk.StringVar()
        self.edad = ctk.StringVar()
        self.peso = ctk.StringVar()
        self.altura = ctk.StringVar()
        self.nombre_dueno = ctk.StringVar()
        self.apellido_dueno = ctk.StringVar()
        self.rut_dueno = ctk.StringVar()
        self.email_dueno = ctk.StringVar()
        self.edad_dueno = ctk.StringVar()

        # -------------- ENCABEZADO ----------------
        encabezado = ctk.CTkFrame(self.root, fg_color="white")
        encabezado.pack(pady=10, fill="x")

        logo = ctk.CTkLabel(encabezado, text="🐾 VETERINARIA APP", font=("Arial", 20, "bold"), text_color="black")
        logo.pack(side="left", padx=20)

        ctk.CTkLabel(self.root, text="Registro de Mascota", font=("Arial", 22, "bold")).pack(pady=5)
        ctk.CTkLabel(self.root, text="Complete los datos de la mascota y su dueño", font=("Arial", 14)).pack()

        # -------------- FORMULARIO ----------------
        form_frame = ctk.CTkFrame(self.root)
        form_frame.pack(pady=20, fill="x", padx=30)

        # --- Datos Mascota ---
        mascota_frame = ctk.CTkFrame(form_frame, fg_color="white")
        mascota_frame.grid(row=0, column=0, padx=20, sticky="n")

        ctk.CTkLabel(mascota_frame, text="Datos de la Mascota", font=("Arial", 16, "bold")).pack(pady=10)

        ctk.CTkLabel(mascota_frame, text="Nombre").pack(anchor="w")
        ctk.CTkEntry(mascota_frame, textvariable=self.nombre_mascota, placeholder_text="Firulais").pack(fill="x")

        ctk.CTkLabel(mascota_frame, text="Edad").pack(anchor="w", pady=(5, 0))
        ctk.CTkEntry(mascota_frame, textvariable=self.edad, placeholder_text="3").pack(fill="x")

        ctk.CTkLabel(mascota_frame, text="Peso (kg)").pack(anchor="w", pady=(5, 0))
        ctk.CTkEntry(mascota_frame, textvariable=self.peso, placeholder_text="12.5").pack(fill="x")

        ctk.CTkLabel(mascota_frame, text="Altura (cm)").pack(anchor="w", pady=(5, 0))
        ctk.CTkEntry(mascota_frame, textvariable=self.altura, placeholder_text="45").pack(fill="x")

        # --- Datos Dueño ---
        dueno_frame = ctk.CTkFrame(form_frame, fg_color="white")
        dueno_frame.grid(row=0, column=1, padx=20, sticky="n")

        ctk.CTkLabel(dueno_frame, text="Datos del Dueño", font=("Arial", 16, "bold")).pack(pady=10)

        ctk.CTkLabel(dueno_frame, text="RUT").pack(anchor="w")
        ctk.CTkEntry(dueno_frame, textvariable=self.rut_dueno, placeholder_text="12345678-9").pack(fill="x")

        ctk.CTkLabel(dueno_frame, text="Nombre").pack(anchor="w")
        ctk.CTkEntry(dueno_frame, textvariable=self.nombre_dueno, placeholder_text="Juan").pack(fill="x")

        ctk.CTkLabel(dueno_frame, text="Apellido").pack(anchor="w")
        ctk.CTkEntry(dueno_frame, textvariable=self.apellido_dueno, placeholder_text="Pérez").pack(fill="x")

        ctk.CTkLabel(dueno_frame, text="Edad").pack(anchor="w")
        ctk.CTkEntry(dueno_frame, textvariable=self.edad_dueno, placeholder_text="30").pack(fill="x")

        ctk.CTkLabel(dueno_frame, text="Email").pack(anchor="w")
        ctk.CTkEntry(dueno_frame, textvariable=self.email_dueno, placeholder_text="juan@mail.com").pack(fill="x")

        # -------------- BOTONES ----------------
        boton_frame = ctk.CTkFrame(self.root, fg_color="white")
        boton_frame.pack(pady=20)

        ctk.CTkButton(boton_frame, text="VOLVER", fg_color="white", text_color="black", border_width=1,
                    border_color="black", width=120, command=self.root.destroy).pack(side="left", padx=10)

        ctk.CTkButton(boton_frame, text="REGISTRAR", fg_color="#007BFF", text_color="white",
                    width=120, command=self.registrar_mascota).pack(side="left", padx=10)

        ctk.CTkButton(boton_frame, text="FINALIZAR", fg_color="black", width=120,
                    command=self.root.destroy).pack(side="left", padx=10)

    def registrar_mascota(self):
        # Validar campos
        campos = [
            self.nombre_mascota.get(), self.edad.get(), self.peso.get(), self.altura.get(),
            self.rut_dueno.get(), self.nombre_dueno.get(), self.apellido_dueno.get(),
            self.edad_dueno.get(), self.email_dueno.get()
        ]
        if not all(campos):
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        try:
            mascota_data = {
                "nombre": self.nombre_mascota.get(),
                "edad": int(self.edad.get()),
                "peso": self.peso.get(),
                "altura": self.altura.get(),
                "raza": "Desconocida",
                "sexo": "Desconocido",
                "dieta": "Normal",
                "caracter": "Tranquilo",
                "habitat": "Casa",
                "id_vet": None  # A definir si hay veterinarios disponibles
            }
            mascota = crud.crear_mascota(db, mascota_data)

            cliente_data = {
                "rut": self.rut_dueno.get(),
                "nombre": self.nombre_dueno.get(),
                "apellido": self.apellido_dueno.get(),
                "edad": int(self.edad_dueno.get()),
                "email": self.email_dueno.get(),
                "tipo": "cliente",
                "id_mascota": mascota.id_mascota
            }
            crud.crear_cliente(db, cliente_data)
            messagebox.showinfo("Éxito", "Mascota y cliente registrados correctamente")

        except Exception as e:
            db.rollback()
            messagebox.showerror("Error", str(e))

if __name__ == '__main__':
    root = ctk.CTk()
    app = VeterinariaApp(root)
    root.mainloop()
