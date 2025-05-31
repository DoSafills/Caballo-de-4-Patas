import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from datetime import datetime

# Activar modo oscuro
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")  

class GestionHorasApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Panel Recepcionista")
        self.root.geometry("750x600")

        ctk.CTkLabel(root, text="Panel Recepcionista", font=("Arial", 20)).pack(pady=20)

        # Frame para formulario
        self.form_frame = ctk.CTkFrame(root)
        self.form_frame.pack(pady=10)

        # Campos del formulario
        self.nombre_entry = self._crear_campo("Nombre del Cliente:", 0)
        self.mascota_entry = self._crear_campo("Nombre de la Mascota:", 1)
        self.fecha_entry = self._crear_campo("Fecha (YYYY-MM-DD):", 2)
        self.hora_entry = self._crear_campo("Hora (HH:MM):", 3)

        # Botones
        self.boton_agendar = ctk.CTkButton(self.form_frame, text="Agendar Hora", command=self.agendar_hora)
        self.boton_agendar.grid(row=4, column=0, columnspan=2, pady=5)

        self.boton_actualizar = ctk.CTkButton(self.form_frame, text="Actualizar Hora", command=self.actualizar_hora)
        self.boton_actualizar.grid(row=5, column=0, columnspan=2, pady=5)

        self.boton_eliminar = ctk.CTkButton(self.form_frame, text="Eliminar Hora", command=self.eliminar_hora)
        self.boton_eliminar.grid(row=6, column=0, columnspan=2, pady=5)

        # Lista de horas agendadas
        self.horas_data = []
        self.listbox = tk.Listbox(root, height=10, width=80)
        self.listbox.pack(pady=10)
        self.listbox.bind("<<ListboxSelect>>", self.seleccionar_hora)

    def _crear_campo(self, label, row):
        ctk.CTkLabel(self.form_frame, text=label).grid(row=row, column=0, padx=10, pady=5, sticky="e")
        entry = ctk.CTkEntry(self.form_frame, width=200)
        entry.grid(row=row, column=1, pady=5)
        return entry

    def validar_fecha_hora(self, fecha_str, hora_str):
        try:
            fecha_hora = datetime.strptime(f"{fecha_str} {hora_str}", "%Y-%m-%d %H:%M")
            return fecha_hora
        except ValueError:
            return None

    def agendar_hora(self):
        nombre = self.nombre_entry.get().strip()
        mascota = self.mascota_entry.get().strip()
        fecha = self.fecha_entry.get().strip()
        hora = self.hora_entry.get().strip()

        if not all([nombre, mascota, fecha, hora]):
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        fecha_hora = self.validar_fecha_hora(fecha, hora)
        if not fecha_hora:
            messagebox.showerror("Error", "Formato de fecha u hora inválido.")
            return

        registro = {
            "fecha_hora": fecha_hora,
            "nombre": nombre,
            "mascota": mascota,
            "estado": "Pendiente atención"  # Puedes cambiar o añadir más estados
        }

        self.horas_data.append(registro)
        self.actualizar_listbox()
        self.limpiar_campos()
        messagebox.showinfo("Éxito", "Hora agendada correctamente.")

    def eliminar_hora(self):
        seleccion = self.listbox.curselection()
        if not seleccion:
            messagebox.showwarning("Atención", "Selecciona una hora para eliminar.")
            return
        index = seleccion[0]
        del self.horas_data[index]
        self.actualizar_listbox()
        self.limpiar_campos()
        messagebox.showinfo("Éxito", "Hora eliminada correctamente.")

    def actualizar_hora(self):
        seleccion = self.listbox.curselection()
        if not seleccion:
            messagebox.showwarning("Atención", "Selecciona una hora para actualizar.")
            return
        index = seleccion[0]

        nombre = self.nombre_entry.get().strip()
        mascota = self.mascota_entry.get().strip()
        fecha = self.fecha_entry.get().strip()
        hora = self.hora_entry.get().strip()

        if not all([nombre, mascota, fecha, hora]):
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        fecha_hora = self.validar_fecha_hora(fecha, hora)
        if not fecha_hora:
            messagebox.showerror("Error", "Formato de fecha u hora inválido.")
            return

        self.horas_data[index].update({
            "fecha_hora": fecha_hora,
            "nombre": nombre,
            "mascota": mascota
        })
        self.actualizar_listbox()
        self.limpiar_campos()
        messagebox.showinfo("Éxito", "Hora actualizada correctamente.")

    def seleccionar_hora(self, event):
        seleccion = self.listbox.curselection()
        if seleccion:
            index = seleccion[0]
            registro = self.horas_data[index]
            fecha_str = registro["fecha_hora"].strftime("%Y-%m-%d")
            hora_str = registro["fecha_hora"].strftime("%H:%M")
            self.fecha_entry.delete(0, "end")
            self.fecha_entry.insert(0, fecha_str)
            self.hora_entry.delete(0, "end")
            self.hora_entry.insert(0, hora_str)
            self.nombre_entry.delete(0, "end")
            self.nombre_entry.insert(0, registro["nombre"])
            self.mascota_entry.delete(0, "end")
            self.mascota_entry.insert(0, registro["mascota"])

    def actualizar_listbox(self):
        self.listbox.delete(0, "end")
        for registro in self.horas_data:
            texto = f"{registro['fecha_hora'].strftime('%Y-%m-%d %H:%M')} - {registro['nombre']} con {registro['mascota']} (Estado: {registro['estado']})"
            self.listbox.insert("end", texto)

    def limpiar_campos(self):
        self.nombre_entry.delete(0, "end")
        self.mascota_entry.delete(0, "end")
        self.fecha_entry.delete(0, "end")
        self.hora_entry.delete(0, "end")

if __name__ == "__main__":
    root = ctk.CTk()
    app = GestionHorasApp(root)
    root.mainloop()