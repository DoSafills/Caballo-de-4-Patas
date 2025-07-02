import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, simpledialog
import requests
from datetime import datetime
from crud import (
    obtener_todos_los_clientes, obtener_mascotas_de_cliente, actualizar_estado_mascota
)
from database import SessionLocal
from factories import VentanaFactory
from controller import MascotaController

API_URL = "http://localhost:8000/recepcionista"

#  FACTORY para futuras creaciones de mascotas (útil si amplías la UI)
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
        # Conexión local para CRUD de clientes/mascotas/estado
        self.db = SessionLocal()
        # Controlador para gestión de mascotas (ventana emergente)
        self.controller = MascotaController(self.db, MascotaFactory)

        self.root = root
        self.root.title("Panel Recepcionista")
        self.root.geometry("950x600")
        ctk.CTkLabel(root, text="Panel Recepcionista", font=("Arial", 20)).pack(pady=20)

        # Inicializar secciones UI
        self._init_frames()
        self._init_form()
        self._init_cliente_section()
        self._init_ver_section()

        # Cargar inicialmente las citas
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
        labels = ["RUT Cliente:", "Nombre Mascota:", "RUT Veterinario:",
                  "RUT Recepcionista:", "Fecha (YYYY-MM-DD):", "Hora (HH:MM):", "Motivo:"]
        ents = []
        for i, lbl in enumerate(labels):
            ctk.CTkLabel(self.form_frame, text=lbl).grid(row=i, column=0, sticky="e", padx=5, pady=5)
            e = ctk.CTkEntry(self.form_frame, width=200)
            e.grid(row=i, column=1, pady=5)
            ents.append(e)
        (self.rut_cliente_entry, self.nombre_mascota_entry,
         self.rut_veterinario_entry, self.rut_recepcionista_entry,
         self.fecha_entry, self.hora_entry, self.motivo_entry) = ents

        ctk.CTkButton(self.form_frame, text="Agendar Hora", command=self.agendar_hora).grid(row=7, column=0, columnspan=2, pady=5)
        ctk.CTkButton(self.form_frame, text="Actualizar Hora", command=self.actualizar_hora).grid(row=8, column=0, columnspan=2, pady=5)
        ctk.CTkButton(self.form_frame, text="Eliminar Hora", command=self.eliminar_hora).grid(row=9, column=0, columnspan=2, pady=5)

        self.listbox = tk.Listbox(self.root, height=10, width=80)
        self.listbox.pack(pady=10)
        self.listbox.bind("<<ListboxSelect>>", self.seleccionar_hora)

    def _init_cliente_section(self):
        ctk.CTkLabel(self.cliente_frame, text="Crear Cliente", font=("Arial", 16)).pack(pady=5)
        labels = ["RUT:", "Nombre:", "Apellido:", "Edad:", "Email:"]
        self.cliente_entries = {}
        for lbl in labels:
            ctk.CTkLabel(self.cliente_frame, text=lbl).pack(anchor="w")
            ent = ctk.CTkEntry(self.cliente_frame, width=200)
            ent.pack(pady=2)
            self.cliente_entries[lbl[:-1].lower()] = ent
        ctk.CTkButton(self.cliente_frame, text="Crear Cliente", command=self.crear_cliente_desde_formulario).pack(pady=5)

    def _init_ver_section(self):
        ctk.CTkButton(self.ver_frame, text="Ver Clientes", command=self.mostrar_clientes).pack(pady=5)
        self.listbox_clientes = tk.Listbox(self.ver_frame, height=6, width=40)
        self.listbox_clientes.pack(pady=5)
        self.listbox_clientes.bind("<<ListboxSelect>>", self.seleccionar_cliente)
        self.listbox_mascotas = tk.Listbox(self.ver_frame, height=6, width=40)
        self.listbox_mascotas.pack(pady=5)
        self.listbox_mascotas.bind("<<ListboxSelect>>", self.seleccionar_mascota)
        ctk.CTkButton(self.ver_frame, text="Gestionar Mascotas", command=self.abrir_gestion_ventana).pack(fill="x", pady=5)

    def crear_cliente_desde_formulario(self):
        try:
            payload = {k: (int(v.get()) if k=='edad' else v.get().strip()) for k,v in self.cliente_entries.items()}
            payload['contrasena'] = '123'
        except ValueError:
            return messagebox.showerror("Error", "Edad debe ser numérica")
        try:
            r = requests.post(f"{API_URL}/clientes/", json=payload)
            if r.ok:
                messagebox.showinfo("Éxito", "Cliente creado")
                for e in self.cliente_entries.values(): e.delete(0, tk.END)
            else:
                messagebox.showerror("Error", r.text)
        except Exception as ex:
            messagebox.showerror("Error", f"API no disponible: {ex}")

    def mostrar_clientes(self):
        self.listbox_clientes.delete(0, tk.END)
        try:
            res = requests.get(f"{API_URL}/clientes/")
            if res.ok:
                for c in res.json():
                    self.listbox_clientes.insert(tk.END, f"{c['rut']} - {c['nombre']} {c['apellido']}")
            else:
                messagebox.showerror("Error", res.text)
        except:
            # Fallback local
            for c in obtener_todos_los_clientes(self.db):
                self.listbox_clientes.insert(tk.END, f"{c.rut} - {c.nombre} {c.apellido}")

    def seleccionar_cliente(self, event):
        sel = self.listbox_clientes.curselection()
        if not sel: return
        rut = self.listbox_clientes.get(sel[0]).split(' - ')[0]
        self.listbox_mascotas.delete(0, tk.END)
        try:
            res = requests.get(f"{API_URL}/clientes/{rut}/mascotas")
            mascotas = res.json() if res.ok else []
            if not mascotas:
                raise Exception
            for m in mascotas:
                self.listbox_mascotas.insert(tk.END, f"{m['nombre']} - Estado: {m['estado']}")
        except:
            for m in obtener_mascotas_de_cliente(self.db, rut):
                self.listbox_mascotas.insert(tk.END, f"{m.nombre} - Estado: {m.estado}")

    def seleccionar_mascota(self, event):
        sel = self.listbox_mascotas.curselection()
        if not sel: return
        nombre = self.listbox_mascotas.get(sel[0]).split(' - ')[0]
        nuevo = simpledialog.askstring("Estado", f"Nuevo estado para {nombre}:")
        if nuevo:
            try:
                r = requests.put(f"{API_URL}/mascotas/{nombre}/estado", json={"estado":nuevo})
                if r.ok:
                    messagebox.showinfo("Éxito", "Estado actualizado")
                else:
                    raise Exception
            except:
                actualizar_estado_mascota(self.db, nombre, nuevo)
                messagebox.showinfo("Éxito", "Estado local actualizado")
            self.mostrar_clientes()

    def cargar_horas(self):
        self.listbox.delete(0, tk.END)
        try:
            res = requests.get(f"{API_URL}/consultas/")
            if res.ok:
                for c in res.json():
                    self.listbox.insert(tk.END, f"ID:{c['id']}, Cliente:{c['cliente']}, Mascota:{c['mascota']}, Vet:{c['veterinario']}, Fecha:{c['fecha_hora']}, Motivo:{c['motivo']}")
            else:
                messagebox.showerror("Error", res.text)
        except Exception as ex:
            messagebox.showerror("Error", f"API no disponible: {ex}")

    def agendar_hora(self):
        data = {
            "id_cliente": None,
            "id_mascota": 1,
            "id_vet": 1,
            "id_recepcionista": 1,
            "fecha_hora": f"{self.fecha_entry.get()}T{self.hora_entry.get()}:00",
            "motivo": self.motivo_entry.get().strip()
        }
        # Intentar obtener id_cliente
        rut = self.rut_cliente_entry.get().strip()
        try:
            r = requests.get(f"{API_URL}/clientes/{rut}")
            if r.ok: data['id_cliente'] = r.json()['id']
            else: return messagebox.showerror("Error", "Cliente no existe")
        except: return messagebox.showerror("Error", "API no responde")
        try:
            r2 = requests.post(f"{API_URL}/consultas/", json=data)
            if r2.ok:
                messagebox.showinfo("Éxito", "Hora agendada")
                self.cargar_horas()
            else:
                messagebox.showerror("Error", r2.text)
        except Exception as ex:
            messagebox.showerror("Error", f"API no disponible: {ex}")

    def actualizar_hora(self):
        sel = self.listbox.curselection()
        if not sel: return messagebox.showerror("Error", "Selecciona cita")
        cita_id = self.listbox.get(sel[0]).split(',')[0].split(':')[1]
        payload = {}
        try:
            r = requests.put(f"{API_URL}/consultas/{cita_id}", json=payload)
            if r.ok:
                messagebox.showinfo("Éxito", "Cita actualizada")
                self.cargar_horas()
            else:
                messagebox.showerror("Error", r.text)
        except Exception as ex:
            messagebox.showerror("Error", f"API no disponible: {ex}")

    def eliminar_hora(self):
        sel = self.listbox.curselection()
        if not sel: return messagebox.showerror("Error", "Selecciona cita")
        cita_id = self.listbox.get(sel[0]).split(',')[0].split(':')[1]
        try:
            r = requests.delete(f"{API_URL}/consultas/{cita_id}")
            if r.ok:
                messagebox.showinfo("Éxito", "Cita eliminada")
                self.cargar_horas()
            else:
                messagebox.showerror("Error", r.text)
        except Exception as ex:
            messagebox.showerror("Error", f"API no disponible: {ex}")

    def seleccionar_hora(self, event):
        # Precarga campos si se requiere
        pass

    def abrir_gestion_ventana(self):
        VentanaFactory.crear("gestion", self.root, self.controller)

if __name__ == "__main__":
    root = ctk.CTk()
    app = GestionHorasApp(root)
    root.mainloop()
