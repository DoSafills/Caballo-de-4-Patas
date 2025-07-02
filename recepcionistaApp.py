import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, simpledialog
import requests
from datetime import datetime

from factories import VentanaFactory
from controller import MascotaController

# URL base de tu API FastAPI
API_URL = "http://localhost:8000/recepcionista"

#  FACTORY (se mantiene para la ventana de gestión de mascotas)
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

# Estilo
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class GestionHorasApp:
    def __init__(self, root):
        # Controlador para la ventana de gestión de mascotas
        self.controller = MascotaController(None, MascotaFactory)

        self.root = root
        self.root.title("Panel Recepcionista")
        self.root.geometry("950x600")
        ctk.CTkLabel(root, text="Panel Recepcionista", font=("Arial", 20)).pack(pady=20)

        # Layout
        self._init_frames()
        self._init_form()
        self._init_cliente_section()
        self._init_ver_section()

        # Cargar datos
        self.cargar_horas()

    def _init_frames(self):
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(pady=10, padx=20, fill="both", expand=True)

        self.form_frame = ctk.CTkFrame(self.main_frame)
        self.form_frame.grid(row=0, column=0, padx=10, pady=10, sticky="n")

        self.cliente_frame = ctk.CTkFrame(self.main_frame)
        self.cliente_frame.grid(row=0, column=1, padx=10, pady=10, sticky="n")

        self.ver_frame = ctk.CTkFrame(self.main_frame)
        self.ver_frame.grid(row=0, column=2, padx=10, pady=10, sticky="n")

    def _init_form(self):
        labels = ["RUT del Cliente:", "Nombre de la Mascota:", "RUT del Veterinario:",
                "RUT del Recepcionista:", "Fecha (YYYY-MM-DD):", "Hora (HH:MM):", "Motivo:"]
        self.entries = {}
        for i, lbl in enumerate(labels):
            ctk.CTkLabel(self.form_frame, text=lbl).grid(row=i, column=0, sticky="e", padx=5, pady=5)
            ent = ctk.CTkEntry(self.form_frame, width=200)
            ent.grid(row=i, column=1, pady=5)
            self.entries[lbl] = ent

        ctk.CTkButton(self.form_frame, text="Agendar Hora",   command=self.agendar_hora).grid(row=7, column=0, columnspan=2, pady=5)
        ctk.CTkButton(self.form_frame, text="Actualizar Hora",command=self.actualizar_hora).grid(row=8, column=0, columnspan=2, pady=5)
        ctk.CTkButton(self.form_frame, text="Eliminar Hora",  command=self.eliminar_hora).grid(row=9, column=0, columnspan=2, pady=5)

        # Listado de citas
        self.listbox = tk.Listbox(self.root, height=10, width=80)
        self.listbox.pack(pady=10)
        self.listbox.bind("<<ListboxSelect>>", self.seleccionar_hora)

    def _init_cliente_section(self):
        ctk.CTkLabel(self.cliente_frame, text="Crear Cliente", font=("Arial", 16)).pack(pady=5)
        campos = ["RUT", "Nombre", "Apellido", "Edad", "Email"]
        self.cliente_entries = {}
        for lbl in campos:
            ctk.CTkLabel(self.cliente_frame, text=f"{lbl}:").pack(anchor="w")
            ent = ctk.CTkEntry(self.cliente_frame, width=200)
            ent.pack(pady=2)
            self.cliente_entries[lbl.lower()] = ent
        ctk.CTkButton(self.cliente_frame, text="Crear Cliente", command=self.crear_cliente_desde_formulario).pack(pady=10)

    def _init_ver_section(self):
        ctk.CTkButton(self.ver_frame, text="Ver Clientes", command=self.mostrar_clientes).pack(pady=5)
        self.listbox_clientes = tk.Listbox(self.ver_frame, height=6, width=40)
        self.listbox_clientes.pack(pady=5)
        self.listbox_clientes.bind("<<ListboxSelect>>", self.seleccionar_cliente)

        self.listbox_mascotas = tk.Listbox(self.ver_frame, height=6, width=40)
        self.listbox_mascotas.pack(pady=5)
        self.listbox_mascotas.bind("<<ListboxSelect>>", self.seleccionar_mascota)

        ctk.CTkButton(self.ver_frame, text="Gestionar Mascotas", command=self.abrir_gestion_ventana).pack(fill="x", pady=5)

    # --- Métodos que llaman a la API ---
    def crear_cliente_desde_formulario(self):
        try:
            payload = {
                "rut":      self.cliente_entries["rut"].get().strip(),
                "nombre":   self.cliente_entries["nombre"].get().strip(),
                "apellido": self.cliente_entries["apellido"].get().strip(),
                "edad":     int(self.cliente_entries["edad"].get().strip()),
                "email":    self.cliente_entries["email"].get().strip(),
                "contrasena": "123"
            }
        except ValueError:
            return messagebox.showerror("Error", "La edad debe ser un número.")

        try:
            r = requests.post(f"{API_URL}/clientes/", json=payload)
            if r.ok:
                messagebox.showinfo("Éxito", "Cliente creado correctamente.")
                for ent in self.cliente_entries.values():
                    ent.delete(0, tk.END)
            else:
                messagebox.showerror("Error", r.text)
        except Exception as ex:
            messagebox.showerror("Error", f"No se pudo conectar: {ex}")

    def mostrar_clientes(self):
        self.listbox_clientes.delete(0, tk.END)
        try:
            r = requests.get(f"{API_URL}/clientes/")
            if r.ok:
                for c in r.json():
                    self.listbox_clientes.insert(tk.END, f"{c['rut']} - {c['nombre']} {c['apellido']}")
            else:
                messagebox.showerror("Error", r.text)
        except:
            messagebox.showerror("Error", "API no disponible para listar clientes.")

    def seleccionar_cliente(self, event):
        sel = self.listbox_clientes.curselection()
        if not sel: return
        rut = self.listbox_clientes.get(sel[0]).split(" - ")[0]
        self.listbox_mascotas.delete(0, tk.END)
        try:
            r = requests.get(f"{API_URL}/clientes/{rut}/mascotas")
            for m in r.json():
                self.listbox_mascotas.insert(tk.END, f"{m['nombre']} - Estado: {m['estado']}")
        except:
            messagebox.showerror("Error", "API no disponible para mascotas.")

    def seleccionar_mascota(self, event):
        sel = self.listbox_mascotas.curselection()
        if not sel: return
        nombre = self.listbox_mascotas.get(sel[0]).split(" - ")[0]
        nuevo = simpledialog.askstring("Actualizar Estado", f"Ingrese nuevo estado para {nombre}:")
        if not nuevo: return
        try:
            r = requests.put(f"{API_URL}/mascotas/{nombre}/estado", json={"estado": nuevo})
            if r.ok:
                messagebox.showinfo("Éxito", "Estado actualizado.")
                self.mostrar_clientes()
            else:
                messagebox.showerror("Error", r.text)
        except:
            messagebox.showerror("Error", "API no disponible para actualizar mascota.")

    def cargar_horas(self):
        self.listbox.delete(0, tk.END)
        try:
            r = requests.get(f"{API_URL}/consultas/")
            if r.ok:
                for c in r.json():
                    texto = (f"ID:{c['id']}, Cliente:{c['cliente']}, Mascota:{c['mascota']}, "
                            f"Vet:{c['veterinario']}, Fecha:{c['fecha_hora']}, Motivo:{c['motivo']}")
                    self.listbox.insert(tk.END, texto)
            else:
                messagebox.showerror("Error", r.text)
        except:
            messagebox.showerror("Error", "API no disponible para listar citas.")

    def agendar_hora(self):
        rut = self.entries["RUT del Cliente:"].get().strip()
        try:
            r = requests.get(f"{API_URL}/clientes/{rut}")
            if not r.ok:
                return messagebox.showerror("Error", "Cliente no existe.")
            cliente_id = r.json()["id"]
        except:
            return messagebox.showerror("Error", "API no disponible.")

        payload = {
            "id_cliente": cliente_id,
            "id_mascota": 1,
            "id_vet": 1,
            "id_recepcionista": 1,
            "fecha_hora": f"{self.entries['Fecha (YYYY-MM-DD):'].get().strip()}T"
                            f"{self.entries['Hora (HH:MM):'].get().strip()}:00",
            "motivo": self.entries["Motivo:"].get().strip()
        }
        try:
            r2 = requests.post(f"{API_URL}/consultas/", json=payload)
            if r2.ok:
                messagebox.showinfo("Éxito", "Hora agendada correctamente.")
                self.cargar_horas()
            else:
                messagebox.showerror("Error", r2.text)
        except:
            messagebox.showerror("Error", "API no disponible para agendar cita.")

    def actualizar_hora(self):
        sel = self.listbox.curselection()
        if not sel: 
            return messagebox.showerror("Error", "Seleccione una cita.")
        cita_id = self.listbox.get(sel[0]).split(",")[0].split(":")[1]
        payload = {}  # aquí podrías enviar cambios de fecha/motivo
        try:
            r = requests.put(f"{API_URL}/consultas/{cita_id}", json=payload)
            if r.ok:
                messagebox.showinfo("Éxito", "Cita actualizada.")
                self.cargar_horas()
            else:
                messagebox.showerror("Error", r.text)
        except:
            messagebox.showerror("Error", "API no disponible para actualizar cita.")

    def eliminar_hora(self):
        sel = self.listbox.curselection()
        if not sel:
            return messagebox.showerror("Error", "Seleccione una cita.")
        cita_id = self.listbox.get(sel[0]).split(",")[0].split(":")[1]
        try:
            r = requests.delete(f"{API_URL}/consultas/{cita_id}")
            if r.ok:
                messagebox.showinfo("Éxito", "Cita eliminada.")
                self.cargar_horas()
            else:
                messagebox.showerror("Error", r.text)
        except:
            messagebox.showerror("Error", "API no disponible para eliminar cita.")

    def seleccionar_hora(self, event):
        # Aquí podrías precargar los campos con la cita seleccionada
        pass

    def abrir_gestion_ventana(self):
        VentanaFactory.crear("gestion", self.root, self.controller)

if __name__ == "__main__":
    root = ctk.CTk()
    app = GestionHorasApp(root)
    root.mainloop()
