import customtkinter as ctk
from tkinter import messagebox
from tkinter import ttk
from controller import MascotaController
import requests
class VentanaGestionMascotas:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller

        self.window = ctk.CTkToplevel()
        self.window.title("Gestión de Mascotas")
        self.window.geometry("800x800")

        ctk.CTkLabel(self.window, text="Gestión de Mascotas", font=("Arial", 18, "bold")).pack(pady=20)

        columnas = ("id", "nombre", "raza", "edad", "sexo", "estado")

        self.tree = ttk.Treeview(self.window, columns=columnas, show="headings", height=10)
        self.tree.pack(padx=20, pady=10, fill="both", expand=False)

        for col in columnas:
            self.tree.heading(col, text=col.capitalize())
            self.tree.column(col, anchor="center")

        self.tree.bind("<Double-1>", self.cargar_mascota)

        # Formulario para modificar datos
        form_frame = ctk.CTkFrame(self.window)
        form_frame.pack(pady=10, padx=20, fill="x")

        self.edad_var = ctk.StringVar()
        self.sexo_var = ctk.StringVar()
        self.estado_var = ctk.StringVar()
        self.historial_nuevo_var = ctk.StringVar()

        ctk.CTkLabel(form_frame, text="Edad").pack(anchor="w")
        ctk.CTkEntry(form_frame, textvariable=self.edad_var).pack(fill="x", pady=5)

        ctk.CTkLabel(form_frame, text="Sexo").pack(anchor="w")
        ctk.CTkComboBox(form_frame, values=["Macho", "Hembra"], variable=self.sexo_var, state="readonly").pack(fill="x", pady=5)

        ctk.CTkLabel(form_frame, text="Estado Médico").pack(anchor="w")
        ctk.CTkComboBox(form_frame, values=["Alta", "Pendiente atención", "En tratamiento"], variable=self.estado_var, state="readonly").pack(fill="x", pady=5)

        ctk.CTkLabel(form_frame, text="Añadir al historial").pack(anchor="w")
        ctk.CTkEntry(form_frame, textvariable=self.historial_nuevo_var, placeholder_text="Ej: Vacunación, Desparasitación...").pack(fill="x", pady=5)

        self.boton_actualizar = ctk.CTkButton(form_frame, text="Guardar Cambios", command=self.actualizar_mascota, fg_color="#27ae60", text_color="white")
        self.boton_actualizar.pack(pady=10)

        self.id_mascota_seleccionada = None

        boton_frame = ctk.CTkFrame(self.window)
        boton_frame.pack(pady=10)

        ctk.CTkButton(boton_frame, text="Actualizar Lista", command=self.mostrar_mascotas, fg_color="#3498db", text_color="white").pack(side="left", padx=10)
        ctk.CTkButton(boton_frame, text="Cerrar", command=self.window.destroy, fg_color="#7f8c8d", text_color="white").pack(side="left", padx=10)

        self.mostrar_mascotas()

    def mostrar_mascotas(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
    # URL base de la API FastAPI
            url = "http://127.0.0.1:8000/veterinaria/mascotas"
            response = requests.get(url)
            response.raise_for_status()  # Lanza excepción si no fue exitosa

            mascotas = response.json()

            if not mascotas:
                messagebox.showinfo("Información", "No hay mascotas registradas.")
                return

            for m in mascotas:
                self.tree.insert("", "end", values=(
                m.get("id_mascota"),
                m.get("nombre"),
                m.get("raza"),
                m.get("edad"),
                m.get("sexo"),
                m.get("estado", "Desconocido")  # Valor por defecto si falta
                ))

        except requests.exceptions.ConnectionError:
            messagebox.showerror("Error de conexión", "No se pudo conectar con la API en http://127.0.0.1:8000.\n¿Está el servidor en ejecución?")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error de petición", f"Error al consultar la API:\n{str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error inesperado:\n{str(e)}")



    def cargar_mascota(self, event):
        selected_item = self.tree.focus()
        if not selected_item:
            return

        values = self.tree.item(selected_item, 'values')
        self.id_mascota_seleccionada = int(values[0])

        mascota = self.controller.db.query(self.controller.model_class).get(self.id_mascota_seleccionada)
        if mascota:
            self.edad_var.set(str(mascota.edad))
            self.sexo_var.set(mascota.sexo)
            self.estado_var.set(mascota.estado)  # Esto puedes cargarlo si se guarda en BD más adelante

    def actualizar_mascota(self):
        if not self.id_mascota_seleccionada:
            messagebox.showwarning("Advertencia", "Seleccione una mascota para modificar.")
            return

        nuevos_datos = {
            "edad": int(self.edad_var.get()),
            "sexo": self.sexo_var.get(),
            "estado": self.estado_var.get()
            # Puedes guardar 'estado_var' si agregas ese campo en el modelo también
        }

        try:
            self.controller.actualizar_mascota(self.id_mascota_seleccionada, nuevos_datos)

            descripcion = self.historial_nuevo_var.get().strip()
            if descripcion:
                self.controller.agregar_historial(self.id_mascota_seleccionada, descripcion)

            messagebox.showinfo("Éxito", "Datos de la mascota actualizados.")
            self.historial_nuevo_var.set("")
            self.mostrar_mascotas()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar: {e}")