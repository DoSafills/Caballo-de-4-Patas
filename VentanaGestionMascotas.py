import customtkinter as ctk
from tkinter import messagebox
from tkinter import ttk

class VentanaGestionMascotas:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller

        self.window = ctk.CTkToplevel()
        self.window.title("Gestión de Mascotas")
        self.window.geometry("800x800")

        ctk.CTkLabel(self.window, text="Gestión de Mascotas", font=("Arial", 18, "bold")).pack(pady=20)

        # Entrada para buscar por ID de mascota
        buscar_frame = ctk.CTkFrame(self.window)
        buscar_frame.pack(pady=10)

        self.id_mascota_buscar = ctk.StringVar()

        ctk.CTkLabel(buscar_frame, text="ID Mascota:").pack(side="left", padx=5)
        ctk.CTkEntry(buscar_frame, textvariable=self.id_mascota_buscar, width=100).pack(side="left", padx=5)
        ctk.CTkButton(buscar_frame, text="Buscar", command=self.buscar_por_id, fg_color="#2980b9").pack(side="left", padx=5)

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

        self.estado_var = ctk.StringVar()
        self.historial_nuevo_var = ctk.StringVar()

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

    def buscar_por_id(self):
        id_str = self.id_mascota_buscar.get().strip()
        if not id_str.isdigit():
            messagebox.showwarning("Entrada inválida", "Por favor ingrese un ID numérico.")
            return

        id_buscar = int(id_str)
        mascota = self.controller.db.query(self.controller.model_class).get(id_buscar)

        for item in self.tree.get_children():
            self.tree.delete(item)

        if mascota:
            self.tree.insert("", "end", values=(
                mascota.id_mascota,
                mascota.nombre,
                mascota.raza,
                mascota.edad,
                mascota.sexo,
                mascota.estado
            ))
        else:
            messagebox.showinfo("Sin resultados", f"No se encontró ninguna mascota con ID {id_buscar}.")

    def mostrar_mascotas(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        mascotas = self.controller.db.query(self.controller.model_class).all()

        if not mascotas:
            messagebox.showinfo("Información", "No hay mascotas registradas.")
        else:
            for m in mascotas:
                self.tree.insert("", "end", values=(
                    m.id_mascota,
                    m.nombre,
                    m.raza,
                    m.edad,
                    m.sexo,
                    m.estado
                ))

    def cargar_mascota(self, event):
        selected_item = self.tree.focus()
        if not selected_item:
            return

        values = self.tree.item(selected_item, 'values')
        self.id_mascota_seleccionada = int(values[0])

        mascota = self.controller.db.query(self.controller.model_class).get(self.id_mascota_seleccionada)
        if mascota:
            self.estado_var.set(mascota.estado)  # Esto puedes cargarlo si se guarda en BD más adelante

    def actualizar_mascota(self):
        if not self.id_mascota_seleccionada:
            messagebox.showwarning("Advertencia", "Seleccione una mascota para modificar.")
            return

        nuevos_datos = {
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