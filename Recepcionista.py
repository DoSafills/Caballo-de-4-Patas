import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from crud import crear_consulta, eliminar_consulta, actualizar_consulta,obtener_cliente_por_rut, obtener_mascota_por_nombre,obtener_veterinario_por_rut, obtener_recepcionista_por_rut
import crud
from database import SessionLocal
from datetime import datetime
from models import Consulta

# Activar modo oscuro
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class GestionHorasApp:
    def __init__(self, root):
        self.db = SessionLocal()
        self.root = root
        self.root.title("Panel Recepcionista")
        self.root.geometry("950x600")

        ctk.CTkLabel(root, text="Panel Recepcionista", font=("Arial", 20)).pack(pady=20)

        # Frame contenedor
        self.main_frame = ctk.CTkFrame(root)
        self.main_frame.pack(pady=10, padx=20, fill="both", expand=True)

        # Frame agendar horas
        self.form_frame = ctk.CTkFrame(self.main_frame)
        self.form_frame.grid(row=0, column=0, padx=10, pady=10, sticky="n")

        # Frame crear cliente
        self.cliente_frame = ctk.CTkFrame(self.main_frame)
        self.cliente_frame.grid(row=0, column=1, padx=10, pady=10, sticky="n")

        # Formulario agendar horas
        self.rut_cliente_entry = self._crear_campo("RUT del Cliente:", 0)
        self.nombre_mascota_entry = self._crear_campo("Nombre de la Mascota:", 1)
        self.rut_veterinario_entry = self._crear_campo("RUT del Veterinario:", 2)
        self.fecha_entry = self._crear_campo("Fecha (YYYY-MM-DD):", 3)
        self.hora_entry = self._crear_campo("Hora (HH:MM):", 4)
        self.motivo_entry = self._crear_campo("Motivo:", 5)

        self.boton_agendar = ctk.CTkButton(self.form_frame, text="Agendar Hora", command=self.agendar_hora)
        self.boton_agendar.grid(row=6, column=0, columnspan=2, pady=5)

        self.boton_actualizar = ctk.CTkButton(self.form_frame, text="Actualizar Hora", command=self.actualizar_hora)
        self.boton_actualizar.grid(row=7, column=0, columnspan=2, pady=5)

        self.boton_eliminar = ctk.CTkButton(self.form_frame, text="Eliminar Hora", command=self.eliminar_hora)
        self.boton_eliminar.grid(row=8, column=0, columnspan=2, pady=5)

        # Lista de horas
        self.horas_data = []
        self.listbox = tk.Listbox(root, height=10, width=80)
        self.listbox.pack(pady=10)
        self.listbox.bind("<<ListboxSelect>>", self.seleccionar_hora)

        # Formulario crear cliente
        ctk.CTkLabel(self.cliente_frame, text="Crear Cliente", font=("Arial", 16)).pack(pady=10)

        self.cliente_rut_entry = self._crear_campo_cliente("RUT:", self.cliente_frame)
        self.cliente_nombre_entry = self._crear_campo_cliente("Nombre:", self.cliente_frame)
        self.cliente_apellido_entry = self._crear_campo_cliente("Apellido:", self.cliente_frame)
        self.cliente_edad_entry = self._crear_campo_cliente("Edad:", self.cliente_frame)
        self.cliente_email_entry = self._crear_campo_cliente("Email:", self.cliente_frame)

        self.boton_crear_cliente = ctk.CTkButton(self.cliente_frame, text="Crear Cliente", command=self.crear_cliente_desde_formulario)
        self.boton_crear_cliente.pack(pady=10)

        self.cargar_horas()

    def _crear_campo(self, label, row):
        ctk.CTkLabel(self.form_frame, text=label).grid(row=row, column=0, padx=10, pady=5, sticky="e")
        entry = ctk.CTkEntry(self.form_frame, width=200)
        entry.grid(row=row, column=1, pady=5)
        return entry

    def _crear_campo_cliente(self, label, frame):
        ctk.CTkLabel(frame, text=label).pack(anchor="w", padx=10, pady=(5, 0))
        entry = ctk.CTkEntry(frame, width=200)
        entry.pack(padx=10, pady=5)
        return entry

    def crear_cliente_desde_formulario(self):
        rut = self.cliente_rut_entry.get().strip()
        nombre = self.cliente_nombre_entry.get().strip()
        apellido = self.cliente_apellido_entry.get().strip()
        edad = self.cliente_edad_entry.get().strip()
        email = self.cliente_email_entry.get().strip()

        if not all([rut, nombre, apellido, edad, email]):
            messagebox.showerror("Error", "Todos los campos del cliente son obligatorios.")
            return

        try:
            edad = int(edad)
        except ValueError:
            messagebox.showerror("Error", "La edad debe ser un número.")
            return

        cliente = crud.crear_cliente(self.db, rut, nombre, apellido, edad, email)
        if cliente:
            messagebox.showinfo("Éxito", "Cliente creado correctamente.")
            self.cliente_rut_entry.delete(0, tk.END)
            self.cliente_nombre_entry.delete(0, tk.END)
            self.cliente_apellido_entry.delete(0, tk.END)
            self.cliente_edad_entry.delete(0, tk.END)
            self.cliente_email_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "No se pudo crear el cliente.")

    def agendar_hora(self):
        rut_cliente = self.rut_cliente_entry.get().strip()
        nombre_mascota = self.nombre_mascota_entry.get().strip()
        rut_vet = self.rut_veterinario_entry.get().strip()
        fecha = self.fecha_entry.get().strip()
        hora = self.hora_entry.get().strip()
        motivo = self.motivo_entry.get().strip()

        if not all([rut_cliente, nombre_mascota, rut_vet, fecha, hora, motivo]):
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        try:
            fecha_hora = datetime.strptime(f"{fecha} {hora}", "%Y-%m-%d %H:%M")
        except ValueError:
            messagebox.showerror("Error", "Formato de fecha u hora inválido.")
            return

        cliente = obtener_cliente_por_rut(self.db, rut_cliente)
        if not cliente:
            messagebox.showerror("Error", "Cliente no encontrado. Debes crearlo primero.")
            return

        mascota = obtener_mascota_por_nombre(self.db, nombre_mascota)
        if not mascota:
            messagebox.showerror("Error", "Mascota no encontrada.")
            return

        vet = obtener_veterinario_por_rut(self.db, rut_vet)
        if not vet:
            messagebox.showerror("Error", "Veterinario no encontrado.")
            return

        recepcionista = obtener_recepcionista_por_rut(self.db, "12345678-9")
        if not recepcionista:
            messagebox.showerror("Error", "Recepcionista no encontrado.")
            return

        try:
            crear_consulta(
                self.db,
                fecha_hora=fecha_hora,
                id_recepcionista=recepcionista.id,
                id_mascota=mascota.id,
                id_vet=vet.id,
                id_cliente=cliente.id,
                motivo=motivo
            )
            messagebox.showinfo("Éxito", "Hora agendada correctamente.")
            self.cargar_horas()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo agendar la hora: {e}")

    def eliminar_hora(self):
        seleccion = self.listbox.curselection()
        if not seleccion:
            messagebox.showwarning("Atención", "Selecciona una hora para eliminar.")
            return
        index = seleccion[0]
        consulta = self.horas_data[index]

        try:
            eliminar_consulta(self.db, consulta.id_consulta)
            messagebox.showinfo("Éxito", "Hora eliminada correctamente.")
            self.cargar_horas()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar la hora: {e}")

    def actualizar_hora(self):
        seleccion = self.listbox.curselection()
        if not seleccion:
            messagebox.showwarning("Atención", "Selecciona una hora para actualizar.")
            return
        index = seleccion[0]
        consulta = self.horas_data[index]

        fecha = self.fecha_entry.get()
        hora = self.hora_entry.get()

        if not all([fecha, hora]):
            messagebox.showerror("Error", "Debes ingresar nueva fecha y hora.")
            return

        try:
            fecha_hora = datetime.strptime(f"{fecha} {hora}", "%Y-%m-%d %H:%M")
        except ValueError:
            messagebox.showerror("Error", "Formato de fecha u hora inválido.")
            return

        nuevos_datos = {
            "fecha_hora": fecha_hora,
            "motivo": "Hora actualizada desde app"
        }
        try:
            actualizar_consulta(self.db, consulta.id_consulta, nuevos_datos)
            messagebox.showinfo("Éxito", "Hora actualizada correctamente.")
            self.cargar_horas()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar la hora: {e}")

    def cargar_horas(self):
        self.listbox.delete(0, tk.END)
        self.horas_data = self.db.query(Consulta).order_by(Consulta.fecha_hora).all()
        for consulta in self.horas_data:
            fecha_str = consulta.fecha_hora.strftime("%Y-%m-%d %H:%M")
            item = f"{fecha_str} - Mascota ID: {consulta.id_mascota} - Cliente ID: {consulta.id_cliente} - Motivo: {consulta.motivo}"
            self.listbox.insert(tk.END, item)

    def seleccionar_hora(self, event):
        seleccion = self.listbox.curselection()
        if not seleccion:
            return
        index = seleccion[0]
        consulta = self.horas_data[index]

        self.fecha_entry.delete(0, tk.END)
        self.fecha_entry.insert(0, consulta.fecha_hora.strftime("%Y-%m-%d"))

        self.hora_entry.delete(0, tk.END)
        self.hora_entry.insert(0, consulta.fecha_hora.strftime("%H:%M"))

if __name__ == "__main__":
    root = ctk.CTk()
    app = GestionHorasApp(root)
    root.mainloop()