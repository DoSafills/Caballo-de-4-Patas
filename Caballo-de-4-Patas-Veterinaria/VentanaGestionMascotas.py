import customtkinter as ctk
from tkinter import messagebox
from tkinter import ttk

class VentanaGestionMascotas:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller

        self.window = ctk.CTkToplevel()
        self.window.title("Gestión de Mascotas")
        self.window.geometry("700x700")

        ctk.CTkLabel(self.window, text="Gestión de Mascotas", font=("Arial", 18, "bold")).pack(pady=20)

        columnas = ("id", "nombre", "raza", "edad", "sexo")

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

        ctk.CTkLabel(form_frame, text="Edad").pack(anchor="w")
        ctk.CTkEntry(form_frame, textvariable=self.edad_var).pack(fill="x", pady=5)

        ctk.CTkLabel(form_frame, text="Sexo").pack(anchor="w")
        ctk.CTkComboBox(form_frame, values=["Macho", "Hembra"], variable=self.sexo_var, state="readonly").pack(fill="x", pady=5)

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
                    m.sexo
                ))

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

    def actualizar_mascota(self):
        if not self.id_mascota_seleccionada:
            messagebox.showwarning("Advertencia", "Seleccione una mascota para modificar.")
            return

        nuevos_datos = {
            "edad": int(self.edad_var.get()),
            "sexo": self.sexo_var.get()
        }

        try:
            self.controller.actualizar_mascota(self.id_mascota_seleccionada, nuevos_datos)
            messagebox.showinfo("Éxito", "Mascota actualizada correctamente.")
            self.mostrar_mascotas()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar: {e}")
