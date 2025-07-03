import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, simpledialog
from crud import (
    crear_consulta, eliminar_consulta, actualizar_consulta,
    obtener_cliente_por_rut, obtener_mascota_por_nombre,
    obtener_veterinario_por_rut, obtener_recepcionista_por_rut,
    crear_cliente,
    obtener_todos_los_clientes, obtener_mascotas_de_cliente, actualizar_estado_mascota
)
from database import SessionLocal
from datetime import datetime
from models import Consulta, Cliente, Mascota, Veterinario, Recepcionista
from factories import VentanaFactory
from controller import MascotaController  # <-- Controlador
import requests
#  FACTORY
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
# Activar modo oscuro
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class GestionHorasApp:
    def __init__(self, root):
        self.db = SessionLocal()
        self.root = root
        self.root.title("Panel Recepcionista")
        self.root.geometry("950x600")
        self.controller = MascotaController(self.db, MascotaFactory)

        ctk.CTkLabel(root, text="Panel Recepcionista", font=("Arial", 20)).pack(pady=20)

        # Frame principal
        self.main_frame = ctk.CTkFrame(root)
        self.main_frame.pack(pady=10, padx=20, fill="both", expand=True)

        # Frame para agendar horas
        self.form_frame = ctk.CTkFrame(self.main_frame)
        self.form_frame.grid(row=0, column=0, padx=10, pady=10, sticky="n")

        # Frame para crear cliente
        self.cliente_frame = ctk.CTkFrame(self.main_frame)
        self.cliente_frame.grid(row=0, column=1, padx=10, pady=10, sticky="n")

        # Frame para ver clientes y mascotas
        self.ver_frame = ctk.CTkFrame(self.main_frame)
        self.ver_frame.grid(row=0, column=2, padx=10, pady=10, sticky="n")

        # Formulario de agendamiento
        self.rut_cliente_entry = self._crear_campo("RUT del Cliente:", 0)
        self.nombre_mascota_entry = self._crear_campo("Nombre de la Mascota:", 1)
        self.rut_veterinario_entry = self._crear_campo("RUT del Veterinario:", 2)
        self.rut_recepcionista_entry = self._crear_campo("RUT del Recepcionista:", 3)
        self.fecha_entry = self._crear_campo("Fecha (YYYY-MM-DD):", 4)
        self.hora_entry = self._crear_campo("Hora (HH:MM):", 5)
        self.motivo_entry = self._crear_campo("Motivo:", 6)

        self.boton_agendar = ctk.CTkButton(self.form_frame, text="Agendar Hora", command=self.agendar_hora)
        self.boton_agendar.grid(row=7, column=0, columnspan=2, pady=5)

        self.boton_actualizar = ctk.CTkButton(self.form_frame, text="Actualizar Hora", command=self.actualizar_hora)
        self.boton_actualizar.grid(row=8, column=0, columnspan=2, pady=5)

        self.boton_eliminar = ctk.CTkButton(self.form_frame, text="Eliminar Hora", command=self.eliminar_hora)
        self.boton_eliminar.grid(row=9, column=0, columnspan=2, pady=5)

        # Lista de horas
        self.horas_data = []
        self.listbox = tk.Listbox(root, height=10, width=80)
        self.listbox.pack(pady=10)
        self.listbox.bind("<<ListboxSelect>>", self.seleccionar_hora)

        # Formulario para crear cliente
        ctk.CTkLabel(self.cliente_frame, text="Crear Cliente", font=("Arial", 16)).pack(pady=10)

        self.cliente_rut_entry = self._crear_campo_cliente("RUT:", self.cliente_frame)
        self.cliente_nombre_entry = self._crear_campo_cliente("Nombre:", self.cliente_frame)
        self.cliente_apellido_entry = self._crear_campo_cliente("Apellido:", self.cliente_frame)
        self.cliente_edad_entry = self._crear_campo_cliente("Edad:", self.cliente_frame)
        self.cliente_email_entry = self._crear_campo_cliente("Email:", self.cliente_frame)
        self.cliente_vet_entry = self._crear_campo_cliente("ID Vet Preferido (opcional):", self.cliente_frame)


        self.boton_crear_cliente = ctk.CTkButton(self.cliente_frame, text="Crear Cliente", command=self.crear_cliente_desde_formulario)
        self.boton_crear_cliente.pack(pady=10)

        # Botón “Ver Clientes”
        self.boton_ver_clientes = ctk.CTkButton(self.ver_frame, text="Ver Clientes", command=self.mostrar_clientes)
        self.boton_ver_clientes.pack(pady=5)

        # Listbox de clientes
        self.listbox_clientes = tk.Listbox(self.ver_frame, height=8, width=40)
        self.listbox_clientes.pack(pady=5)
        self.listbox_clientes.bind("<<ListboxSelect>>", self.seleccionar_cliente)

        # Listbox para mostrar mascotas de ese cliente (y su estado)
        self.listbox_mascotas = tk.Listbox(self.ver_frame, height=8, width=40)
        self.listbox_mascotas.pack(pady=5)
        self.listbox_mascotas.bind("<<ListboxSelect>>", self.seleccionar_mascota)

        self.cargar_horas()
        ctk.CTkButton(self.ver_frame, text="Gestionar Mascotas", command=self.abrir_gestion_ventana, fg_color="#2980b9", text_color="white").pack(pady=5, fill="x")

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
        vet_preferido = self.cliente_vet_entry.get().strip()

        if not all([rut, nombre, apellido, edad, email]):
            messagebox.showerror("Error", "Todos los campos obligatorios deben estar completos.")
            return

        try:
            edad = int(edad)
        except ValueError:
            messagebox.showerror("Error", "La edad debe ser un número.")
            return

        data = {
            "rut": rut,
            "nombre": nombre,
            "apellido": apellido,
            "edad": edad,
            "email": email,
            "rut_vet_preferido": vet_preferido if vet_preferido else None
        }

        try:
            response = requests.post("http://127.0.0.1:8000/recepcionista/clientes/", json=data)
            response.raise_for_status()  # lanza error si status >= 400
            messagebox.showinfo("Éxito", "Cliente creado correctamente.")
            for entry in [self.cliente_rut_entry, self.cliente_nombre_entry, self.cliente_apellido_entry, self.cliente_edad_entry, self.cliente_email_entry, self.cliente_vet_entry]:
                entry.delete(0, tk.END)
        except requests.exceptions.HTTPError as errh:
            detail = response.json().get("detail", "No se pudo crear el cliente.")
            messagebox.showerror("Error HTTP", detail)
        except requests.exceptions.RequestException as err:
            messagebox.showerror("Error", f"No se pudo conectar al servidor: {err}")

    def agendar_hora(self):
        rut_cliente = self.rut_cliente_entry.get().strip()
        nombre_mascota = self.nombre_mascota_entry.get().strip()
        rut_vet = self.rut_veterinario_entry.get().strip()
        rut_recep = self.rut_recepcionista_entry.get().strip()
        fecha = self.fecha_entry.get().strip()
        hora = self.hora_entry.get().strip()
        motivo = self.motivo_entry.get().strip()

        if not all([rut_cliente, nombre_mascota, rut_vet, rut_recep, fecha, hora, motivo]):
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

        recepcionista = obtener_recepcionista_por_rut(self.db, rut_recep)
        if not recepcionista:
            messagebox.showerror("Error", "Recepcionista no encontrado.")
            return

        consulta = Consulta(
            id_cliente=cliente.id,
            id_mascota=mascota.id,
            id_veterinario=vet.id,
            id_recepcionista=recepcionista.id,
            fecha_hora=fecha_hora,
            motivo=motivo
        )
        crear_consulta(self.db, consulta)
        messagebox.showinfo("Éxito", "Hora agendada correctamente.")
        self.limpiar_campos_formulario()
        self.cargar_horas()

    def actualizar_hora(self):
        try:
            seleccion = self.listbox.curselection()
            if not seleccion:
                messagebox.showerror("Error", "Debes seleccionar una hora para actualizar.")
                return

            index = seleccion[0]
            consulta = self.horas_data[index]

            rut_cliente = self.rut_cliente_entry.get().strip()
            nombre_mascota = self.nombre_mascota_entry.get().strip()
            rut_vet = self.rut_veterinario_entry.get().strip()
            rut_recep = self.rut_recepcionista_entry.get().strip()
            fecha = self.fecha_entry.get().strip()
            hora = self.hora_entry.get().strip()
            motivo = self.motivo_entry.get().strip()

            if not all([rut_cliente, nombre_mascota, rut_vet, rut_recep, fecha, hora, motivo]):
                messagebox.showerror("Error", "Todos los campos son obligatorios.")
                return

            fecha_hora = datetime.strptime(f"{fecha} {hora}", "%Y-%m-%d %H:%M")

            cliente = obtener_cliente_por_rut(self.db, rut_cliente)
            mascota = obtener_mascota_por_nombre(self.db, nombre_mascota)
            vet = obtener_veterinario_por_rut(self.db, rut_vet)
            recepcionista = obtener_recepcionista_por_rut(self.db, rut_recep)

            if not all([cliente, mascota, vet, recepcionista]):
                messagebox.showerror("Error", "Uno o más datos no existen en la base de datos.")
                return

            consulta.id_cliente = cliente.id
            consulta.id_mascota = mascota.id
            consulta.id_veterinario = vet.id
            consulta.id_recepcionista = recepcionista.id
            consulta.fecha_hora = fecha_hora
            consulta.motivo = motivo

            actualizar_consulta(self.db, consulta)
            messagebox.showinfo("Éxito", "Hora actualizada correctamente.")
            self.limpiar_campos_formulario()
            self.cargar_horas()

        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")

    def eliminar_hora(self):
        seleccion = self.listbox.curselection()
        if not seleccion:
            messagebox.showerror("Error", "Debes seleccionar una hora para eliminar.")
            return

        index = seleccion[0]
        consulta = self.horas_data[index]
        eliminar_consulta(self.db, consulta)
        messagebox.showinfo("Éxito", "Hora eliminada correctamente.")
        self.limpiar_campos_formulario()
        self.cargar_horas()

    def cargar_horas(self):
        self.listbox.delete(0, tk.END)
        self.horas_data = []

        try:
            response = requests.get("http://127.0.0.1:8000/recepcionista/consultas/")
            response.raise_for_status()
            consultas = response.json()

            for c in consultas:
        # Formatear fecha y hora de forma segura
                try:
                    fecha_str = datetime.fromisoformat(c["fecha_hora"]).strftime("%Y-%m-%d %H:%M")
                except Exception:
                    fecha_str = c["fecha_hora"]  # fallback sin formato

                display_text = (
                    f"ID: {c['id_consulta']}, Cliente: {c['id_cliente']}, "
                    f"Mascota: {c['id_mascota']}, Vet: {c['id_vet']}, "
                    f"Fecha y Hora: {fecha_str}, Motivo: {c['motivo']}"
                )
                self.listbox.insert(tk.END, display_text)
                self.horas_data.append(c)

        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"No se pudieron cargar las consultas:\n{e}")

    def limpiar_campos_formulario(self):
        for entry in [self.rut_cliente_entry, self.nombre_mascota_entry, self.rut_veterinario_entry, self.rut_recepcionista_entry, self.fecha_entry, self.hora_entry, self.motivo_entry]:
            entry.delete(0, tk.END)

    def seleccionar_hora(self, event):
        seleccion = self.listbox.curselection()
        if not seleccion:
            return
        index = seleccion[0]
        consulta = self.horas_data[index]

        cliente = self.db.query(obtener_cliente_por_rut).filter_by(id=consulta.id_cliente).first()
        mascota = self.db.query(obtener_mascota_por_nombre).filter_by(id=consulta.id_mascota).first()
        vet = self.db.query(obtener_veterinario_por_rut).filter_by(id=consulta.id_veterinario).first()
        recepcionista = self.db.query(obtener_recepcionista_por_rut).filter_by(id=consulta.id_recepcionista).first()

        self.rut_cliente_entry.delete(0, tk.END)
        self.rut_cliente_entry.insert(0, cliente.rut if cliente else "")

        self.nombre_mascota_entry.delete(0, tk.END)
        self.nombre_mascota_entry.insert(0, mascota.nombre if mascota else "")

        self.rut_veterinario_entry.delete(0, tk.END)
        self.rut_veterinario_entry.insert(0, vet.rut if vet else "")

        self.rut_recepcionista_entry.delete(0, tk.END)
        self.rut_recepcionista_entry.insert(0, recepcionista.rut if recepcionista else "")

        fecha_str = consulta.fecha_hora.strftime("%Y-%m-%d")
        hora_str = consulta.fecha_hora.strftime("%H:%M")

        self.fecha_entry.delete(0, tk.END)
        self.fecha_entry.insert(0, fecha_str)

        self.hora_entry.delete(0, tk.END)
        self.hora_entry.insert(0, hora_str)

        self.motivo_entry.delete(0, tk.END)
        self.motivo_entry.insert(0, consulta.motivo)

    def mostrar_clientes(self):
        self.listbox_clientes.delete(0, tk.END)

        try:
            response = requests.get("http://127.0.0.1:8000/recepcionista/clientes/")
            response.raise_for_status()  # lanza excepción si hay error

            clientes = response.json()  # lista de dicts

            for cliente in clientes:
                self.listbox_clientes.insert(tk.END, f"{cliente['rut']} - {cliente['nombre']} {cliente['apellido']}")

        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"No se pudo obtener la lista de clientes:\n{e}")

    def seleccionar_cliente(self, event):
        seleccion = self.listbox_clientes.curselection()
        if not seleccion:
            return
        index = seleccion[0]
        cliente_str = self.listbox_clientes.get(index)
        rut_cliente = cliente_str.split(" - ")[0]

        mascotas = obtener_mascotas_de_cliente(self.db, rut_cliente)
        self.listbox_mascotas.delete(0, tk.END)
        for mascota in mascotas:
            self.listbox_mascotas.insert(tk.END, f"{mascota.nombre} - Estado: {mascota.estado}")

    def seleccionar_mascota(self, event):
        seleccion = self.listbox_mascotas.curselection()
        if not seleccion:
            return
        index = seleccion[0]
        mascota_str = self.listbox_mascotas.get(index)
        nombre_mascota = mascota_str.split(" - ")[0]

        # Aquí preguntar si desea cambiar el estado
        nuevo_estado = simpledialog.askstring("Actualizar Estado", f"Ingrese nuevo estado para {nombre_mascota}:")
        if nuevo_estado:
            actualizar_estado_mascota(self.db, nombre_mascota, nuevo_estado)
            messagebox.showinfo("Éxito", f"Estado de {nombre_mascota} actualizado a {nuevo_estado}.")
            # Actualizar lista de mascotas
            self.mostrar_clientes()
    def abrir_gestion_ventana(self):
        VentanaFactory.crear("gestion", self.root, self.controller)

if __name__ == "__main__":
    root = ctk.CTk()
    app = GestionHorasApp(root)
    root.mainloop()
