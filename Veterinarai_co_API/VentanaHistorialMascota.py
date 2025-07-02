import customtkinter as ctk
from tkinter import messagebox
from tkinter import ttk
import datetime
import requests 

class VentanaHistorialMascota:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller

        self.window = ctk.CTkToplevel()
        self.window.title("Historial Médico de Mascota")
        self.window.geometry("700x650")

        ctk.CTkLabel(self.window, text="Historial Médico", font=("Arial", 18, "bold")).pack(pady=20)

        # Entrada de ID de mascota
        entrada_frame = ctk.CTkFrame(self.window)
        entrada_frame.pack(pady=10)
        self.id_mascota = ctk.StringVar()

        ctk.CTkLabel(entrada_frame, text="ID Mascota:").pack(side="left", padx=5)
        ctk.CTkEntry(entrada_frame, textvariable=self.id_mascota, width=100).pack(side="left", padx=5)
        ctk.CTkButton(entrada_frame, text="Buscar", command=self.mostrar_historial, fg_color="#2980b9").pack(side="left", padx=5)

        # Tabla de historial
        columnas = ("id", "fecha", "descripcion")
        self.tree = ttk.Treeview(self.window, columns=columnas, show="headings", height=10)
        for col in columnas:
            self.tree.heading(col, text=col.capitalize())
            self.tree.column(col, anchor="center")
        self.tree.pack(padx=20, pady=10, fill="both", expand=False)

        # Formulario para nueva entrada
        form = ctk.CTkFrame(self.window)
        form.pack(padx=20, pady=10, fill="x")

        self.descripcion_var = ctk.StringVar()

        ctk.CTkLabel(form, text="Nueva Atención (Descripción):").pack(anchor="w")
        ctk.CTkEntry(form, textvariable=self.descripcion_var).pack(fill="x", pady=5)

        ctk.CTkButton(form, text="Registrar Atención", command=self.agregar_historial, fg_color="#27ae60", text_color="white").pack(pady=10)

    def mostrar_historial(self):
        mascota_id = self.id_mascota.get()
        if not mascota_id.isdigit():
            messagebox.showerror("Error", "Ingrese un ID de mascota válido.")
            return

        try:
            response = requests.get(f"http://127.0.0.1:8000/historial/{mascota_id}")
            if response.status_code == 200:
                historiales = response.json()
                self.tree.delete(*self.tree.get_children())
                for h in historiales:
                    self.tree.insert("", "end", values=(h["id_historial"], h["fecha"], h["descripcion"]))
            else:
                detalle = response.json().get("detail", "Historial no encontrado.")
                messagebox.showinfo("Sin resultados", f"{detalle}")
                self.tree.delete(*self.tree.get_children())
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo conectar con la API:\n{e}")



    def agregar_historial(self):
        mascota_id = self.id_mascota.get()
        descripcion = self.descripcion_var.get().strip()
     
        if not (mascota_id.isdigit() and descripcion):
            messagebox.showerror("Error", "Ingrese un ID de mascota válido y una descripción.")
            return
     
        datos = {
            "descripcion": descripcion,
            "id_mascota": int(mascota_id)
        }
     
        try:
            response = requests.post("http://127.0.0.1:8000/historial/", json=datos)
            if response.status_code == 200:
                messagebox.showinfo("Éxito", "Atención registrada.")
                self.descripcion_var.set("")
                self.mostrar_historial()
            else:
                detalle = response.json().get("detail", "No se pudo registrar.")
                messagebox.showerror("Error", f"Servidor: {detalle}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo conectar con la API:\n{e}")

