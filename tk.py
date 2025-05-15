import customtkinter as ctk
from tkinter import messagebox

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

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

        # Nuevas variables (Agregado)
        self.nombre_dueno = ctk.StringVar()  # <-- NUEVO
        self.telefono_dueno = ctk.StringVar()  # <-- NUEVO

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

        # --- Datos Dueño (Agregado) ---
        dueno_frame = ctk.CTkFrame(form_frame, fg_color="white")
        dueno_frame.grid(row=0, column=1, padx=20, sticky="n")

        ctk.CTkLabel(dueno_frame, text="Datos del Dueño", font=("Arial", 16, "bold")).pack(pady=10)

        ctk.CTkLabel(dueno_frame, text="Nombre Completo").pack(anchor="w")
        ctk.CTkEntry(dueno_frame, textvariable=self.nombre_dueno, placeholder_text="Juan Pérez").pack(fill="x")

        ctk.CTkLabel(dueno_frame, text="Teléfono").pack(anchor="w", pady=(5, 0))
        ctk.CTkEntry(dueno_frame, textvariable=self.telefono_dueno, placeholder_text="+56 9 xxxx xxxx").pack(fill="x")

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
        if not all([
            self.nombre_mascota.get(),
            self.edad.get(),
            self.peso.get(),
            self.altura.get(),
            self.nombre_dueno.get(),  # <-- Validación NUEVO
            self.telefono_dueno.get()  # <-- Validación NUEVO
        ]):
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        try:
            # Se usa el teléfono del dueño como ID temporal
            crear_mascota(
                self.db,
                nombre=self.nombre_mascota.get(),
                id_mascota=self.telefono_dueno.get(),  # <-- REUSO para id_mascota
                edad=int(self.edad.get()),
                peso=float(self.peso.get()),
                altura=float(self.altura.get()),
                nombre_dueno=self.nombre_dueno.get(),  # <-- NUEVO parámetro
                telefono_dueno=self.telefono_dueno.get()  # <-- NUEVO parámetro
            )
            messagebox.showinfo("Éxito", "Mascota registrada correctamente")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def cerrar(self):
        self.db.close()

if __name__ == '__main__':
    root = ctk.CTk()
    app = VeterinariaApp(root)
    root.protocol("WM_DELETE_WINDOW", lambda: (app.cerrar(), root.destroy()))
    root.mainloop()
