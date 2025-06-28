import customtkinter as ctk
from tkinter import messagebox
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

import os


ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
db_path = os.path.join(parent_dir, "veterinaria.db")




class VeterinariaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Asistencia de Reserva")
        self.root.geometry("800x700")
        self.root.configure(bg="#f7f7f7")
    

        self.nombre_mascota = ctk.StringVar()
        self.raza = ctk.StringVar()
        self.sexo = ctk.StringVar()
        self.edad = ctk.StringVar()
        self.vacunas = ctk.BooleanVar()
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

        progress_frame = ctk.CTkFrame(container, fg_color="#ffffff")
        progress_frame.pack(pady=10)
        steps = ["ESPECIALIDAD", "PROFESIONAL", "FECHA Y HORA", "DATOS"]
        for i, step in enumerate(steps):
            ctk.CTkLabel(progress_frame, text="●", text_color="#f57c00", font=("Arial", 18)).pack(side="left")
            ctk.CTkLabel(progress_frame, text=step, text_color="#000", font=("Arial", 12, "bold"), padx=10).pack(side="left")
            if i < len(steps) - 1:
                ctk.CTkLabel(progress_frame, text="▬" * 5, text_color="#f57c00").pack(side="left")

        form_frame = ctk.CTkFrame(container, fg_color="#ffffff")
        form_frame.pack(padx=30, pady=20, fill="both")

        mascota_frame = ctk.CTkFrame(form_frame, fg_color="#ffffff")
        mascota_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        duenio_frame = ctk.CTkFrame(form_frame, fg_color="#ffffff")
        duenio_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        form_frame.grid_columnconfigure(0, weight=1)
        form_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(mascota_frame, text="Datos de la Mascota", font=("Arial", 16, "bold"), text_color="#000").pack(anchor="w", pady=(0, 10))

        row1 = ctk.CTkFrame(mascota_frame, fg_color="#ffffff")
        row1.pack(fill="x", pady=4)
        ctk.CTkLabel(row1, text="Nombre:", text_color="#666", width=100).pack(side="left")
        ctk.CTkEntry(row1, textvariable=self.nombre_mascota, placeholder_text="Fido", width=160).pack(side="left", padx=10)

        row2 = ctk.CTkFrame(mascota_frame, fg_color="#ffffff")
        row2.pack(fill="x", pady=4)
        ctk.CTkLabel(row2, text="Raza:", text_color="#666", width=100).pack(side="left")
        ctk.CTkEntry(row2, textvariable=self.raza, placeholder_text="Golden", width=160).pack(side="left", padx=10)

        row3 = ctk.CTkFrame(mascota_frame, fg_color="#ffffff")
        row3.pack(fill="x", pady=4)
        ctk.CTkLabel(row3, text="Sexo:", text_color="#666", width=100).pack(side="left")
        sexo_frame = ctk.CTkFrame(row3, fg_color="#ffffff")
        sexo_frame.pack(side="left")
        ctk.CTkRadioButton(sexo_frame, text="Macho", value="Macho", variable=self.sexo).pack(side="left", padx=5)
        ctk.CTkRadioButton(sexo_frame, text="Hembra", value="Hembra", variable=self.sexo).pack(side="left", padx=5)

        row4 = ctk.CTkFrame(mascota_frame, fg_color="#ffffff")
        row4.pack(fill="x", pady=4)
        ctk.CTkLabel(row4, text="Edad:", text_color="#666", width=100).pack(side="left")
        ctk.CTkComboBox(row4, values=[f"{i} años" for i in range(1, 21)], variable=self.edad, width=160).pack(side="left", padx=10)

        ctk.CTkCheckBox(mascota_frame, text="Tiene sus vacunas al día", variable=self.vacunas).pack(anchor="w", pady=10)

        ctk.CTkLabel(duenio_frame, text="Datos de Dueño", font=("Arial", 16, "bold"), text_color="#000").pack(anchor="w", pady=(0, 10))

        for label, var, placeholder in [
            ("Nombre Completo:", self.nombre_duenio, "Alejandra Saavedra Villar"),
            ("Email:", self.email_duenio, "aleja_12@gmail.com"),
            ("Teléfono:", self.telefono_duenio, "+51 990656893")
        ]:
            row = ctk.CTkFrame(duenio_frame, fg_color="#ffffff")
            row.pack(fill="x", pady=4)
            ctk.CTkLabel(row, text=label, text_color="#666", width=120).pack(side="left")
            ctk.CTkEntry(row, textvariable=var, placeholder_text=placeholder, width=180).pack(side="left", padx=10)

        botones = ctk.CTkFrame(container, fg_color="#ffffff")
        botones.pack(pady=10, padx=20, fill="x")
        ctk.CTkButton(botones, text="VOLVER", fg_color="#ffffff", text_color="#000", border_width=1, border_color="#000", width=120).pack(side="left")
        ctk.CTkButton(botones, text="FINALIZAR", fg_color="#f57c00", text_color="#ffffff", hover_color="#e65100", width=120, command=self.registrar_mascota).pack(side="right")

    def registrar_mascota(self):
        if not all([
            self.nombre_mascota.get(), self.raza.get(), self.sexo.get(), self.edad.get(),
            self.nombre_duenio.get(), self.email_duenio.get(), self.telefono_duenio.get()
        ]):
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        try:
            datos = {
                "nombre": self.nombre_mascota.get(),
                "raza": self.raza.get(),
                "sexo": self.sexo.get(),
                "edad": self.edad.get(),
                "vacunas": self.vacunas.get(),
                "duenio": self.nombre_duenio.get(),
                "email": self.email_duenio.get(),
                "telefono": self.telefono_duenio.get()
            }
            self.controller.registrar_mascota(datos)
            messagebox.showinfo("Éxito", "Mascota registrada exitosamente")
        except Exception as e:
            db.rollback()
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = ctk.CTk()
    app = VeterinariaApp(root)
    root.mainloop()