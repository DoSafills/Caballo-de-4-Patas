import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import re

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# ------------------- CHAIN OF RESPONSIBILITY -------------------

class Handler:
    def __init__(self):
        self._next = None

    def set_next(self, handler):
        self._next = handler
        return handler

    def handle(self, data):
        if self._next:
            return self._next.handle(data)
        return True

class CamposVaciosValidator(Handler):
    def handle(self, data):
        if not all([data["nombre"], data["mascota"], data["fecha"], data["hora"]]):
            raise ValueError("Todos los campos son obligatorios.")
        return super().handle(data)

class FechaValidator(Handler):
    def handle(self, data):
        if not re.match(r"\d{4}-\d{2}-\d{2}$", data["fecha"]):
            raise ValueError("Formato de fecha inválido. Use YYYY-MM-DD.")
        return super().handle(data)

class HoraValidator(Handler):
    def handle(self, data):
        if not re.match(r"\d{2}:\d{2}$", data["hora"]):
            raise ValueError("Formato de hora inválido. Use HH:MM.")
        return super().handle(data)

# ------------------- ITERATOR PARA HORAS -------------------

class HoraIterator:
    def __init__(self, horas):
        self._horas = horas
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._index < len(self._horas):
            hora = self._horas[self._index]
            self._index += 1
            return hora
        else:
            raise StopIteration

class ColeccionHoras:
    def __init__(self, horas):
        self._horas = horas

    def __iter__(self):
        return HoraIterator(self._horas)

# ------------------- VENTANA RECEPCIONISTA -------------------

class GestionHorasApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Panel Recepcionista")
        self.root.geometry("750x600")

        ctk.CTkLabel(root, text="Panel Recepcionista", font=("Arial", 20)).pack(pady=20)

        self.form_frame = ctk.CTkFrame(root)
        self.form_frame.pack(pady=10)

        self.nombre_entry = self._crear_campo("Nombre del Cliente:", 0)
        self.mascota_entry = self._crear_campo("Nombre de la Mascota:", 1)
        self.fecha_entry = self._crear_campo("Fecha (YYYY-MM-DD):", 2)
        self.hora_entry = self._crear_campo("Hora (HH:MM):", 3)

        self.boton_agendar = ctk.CTkButton(self.form_frame, text="Agendar Hora", command=self.agendar_hora)
        self.boton_agendar.grid(row=4, column=0, columnspan=2, pady=5)

        self.boton_actualizar = ctk.CTkButton(self.form_frame, text="Actualizar Hora", command=self.actualizar_hora)
        self.boton_actualizar.grid(row=5, column=0, columnspan=2, pady=5)

        self.boton_eliminar = ctk.CTkButton(self.form_frame, text="Eliminar Hora", command=self.eliminar_hora)
        self.boton_eliminar.grid(row=6, column=0, columnspan=2, pady=5)

        self.horas_data = []
        self.listbox = tk.Listbox(root, height=10, width=80)
        self.listbox.pack(pady=10)
        self.listbox.bind("<<ListboxSelect>>", self.seleccionar_hora)

    def _crear_campo(self, label, row):
        ctk.CTkLabel(self.form_frame, text=label).grid(row=row, column=0, padx=10, pady=5, sticky="e")
        entry = ctk.CTkEntry(self.form_frame, width=200)
        entry.grid(row=row, column=1, pady=5)
        return entry

    def _validar(self, datos):
        validador = CamposVaciosValidator()
        validador.set_next(FechaValidator()).set_next(HoraValidator())
        validador.handle(datos)

    def agendar_hora(self):
        datos = {
            "nombre": self.nombre_entry.get(),
            "mascota": self.mascota_entry.get(),
            "fecha": self.fecha_entry.get(),
            "hora": self.hora_entry.get()
        }

        try:
            self._validar(datos)
            registro = f"{datos['fecha']} {datos['hora']} - {datos['nombre']} con {datos['mascota']}"
            self.horas_data.append(registro)
            self.actualizar_listbox()
            self.limpiar_campos()
            messagebox.showinfo("Éxito", "Hora agendada correctamente.")
        except ValueError as e:
            messagebox.showerror("Validación fallida", str(e))

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

        datos = {
            "nombre": self.nombre_entry.get(),
            "mascota": self.mascota_entry.get(),
            "fecha": self.fecha_entry.get(),
            "hora": self.hora_entry.get()
        }

        try:
            self._validar(datos)
            index = seleccion[0]
            self.horas_data[index] = f"{datos['fecha']} {datos['hora']} - {datos['nombre']} con {datos['mascota']}"
            self.actualizar_listbox()
            self.limpiar_campos()
            messagebox.showinfo("Éxito", "Hora actualizada correctamente.")
        except ValueError as e:
            messagebox.showerror("Validación fallida", str(e))

    def seleccionar_hora(self, event):
        seleccion = self.listbox.curselection()
        if seleccion:
            texto = self.listbox.get(seleccion[0])
            try:
                fecha_hora, resto = texto.split(" - ")
                nombre, mascota = resto.split(" con ")
                fecha, hora = fecha_hora.split()
                self.fecha_entry.delete(0, "end")
                self.fecha_entry.insert(0, fecha)
                self.hora_entry.delete(0, "end")
                self.hora_entry.insert(0, hora)
                self.nombre_entry.delete(0, "end")
                self.nombre_entry.insert(0, nombre)
                self.mascota_entry.delete(0, "end")
                self.mascota_entry.insert(0, mascota)
            except Exception:
                pass

    def actualizar_listbox(self):
        self.listbox.delete(0, "end")
        for hora in ColeccionHoras(self.horas_data):
            self.listbox.insert("end", hora)

    def limpiar_campos(self):
        self.nombre_entry.delete(0, "end")
        self.mascota_entry.delete(0, "end")
        self.fecha_entry.delete(0, "end")
        self.hora_entry.delete(0, "end")

# Ejecutar aplicación
if __name__ == "__main__":
    root = ctk.CTk()
    app = GestionHorasApp(root)
    root.mainloop()
