import customtkinter as ctk
from crud import obtener_usuarios_por_tipo, eliminar_usuario, actualizar_usuario, crear_usuario
from database import SessionLocal
from tkinter import messagebox
from iterator import ColeccionUsuarios
import requests

API_URL = "http://127.0.0.1:8000"

class AdminApp(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.db = SessionLocal()
        self.pack(fill="both", expand=True)

        self.tipo_usuario = ctk.StringVar(value="todos")
        self.tipo_crear = ctk.StringVar(value="admin")

        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure(1, weight=1)

        # panel izquierdo
        izquierda = ctk.CTkFrame(self)
        izquierda.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.selector_tipo = ctk.CTkOptionMenu(izquierda, values=["todos", "admin", "cliente", "mascota", "recepcionista", "veterinario"], variable=self.tipo_usuario, command=self.cargar_usuarios)
        self.selector_tipo.pack(pady=5)

        self.rut_entry = ctk.CTkEntry(izquierda, placeholder_text="rut del usuario")
        self.rut_entry.pack(pady=5)

        self.boton_actualizar = ctk.CTkButton(izquierda, text="actualizar", command=self.actualizar)
        self.boton_actualizar.pack(pady=5)

        self.boton_eliminar = ctk.CTkButton(izquierda, text="eliminar", command=self.eliminar)
        self.boton_eliminar.pack(pady=5)

        # panel derecho
        derecha = ctk.CTkFrame(self)
        derecha.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        ctk.CTkLabel(derecha, text="crear nuevo usuario").pack(pady=5)

        self.crear_tipo = ctk.CTkOptionMenu(derecha, values=["admin", "recepcionista", "veterinario"], variable=self.tipo_crear)
        self.crear_tipo.pack(pady=5)

        self.crear_entries = {}
        for campo in ["rut", "nombre", "apellido", "edad", "email", "contrasena", "especializacion"]:
            entry = ctk.CTkEntry(derecha, placeholder_text=campo)
            entry.pack(pady=2)
            self.crear_entries[campo] = entry

        self.boton_crear = ctk.CTkButton(derecha, text="crear usuario", command=self.crear)
        self.boton_crear.pack(pady=5)

        # tabla (vista de usuarios) con tamaño fijo
        self.frame_tabla = ctk.CTkScrollableFrame(self, width=800, height=300)
        self.frame_tabla.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)
        self.frame_tabla.grid_columnconfigure((0, 1, 2), weight=1)

        self.cargar_usuarios("todos")


    
    def cargar_usuarios(self, tipo):
        for widget in self.frame_tabla.winfo_children():
            widget.destroy()

        encabezados = ["tipo", "rut", "nombre"]
        for i, texto in enumerate(encabezados):
            ctk.CTkLabel(self.frame_tabla, text=texto.upper(), font=ctk.CTkFont(weight="bold")).grid(row=0, column=i, padx=5, pady=5)

        tipos = [tipo] if tipo != "todos" else ["admin", "recepcionista", "veterinario", "cliente", "mascota"]
        fila = 1

        for t in tipos:
            try:
                res = requests.get(f"http://127.0.0.1:8000/admin/usuarios/{t}")
                if res.status_code == 200:
                    usuarios = res.json()
                    for usuario in usuarios:
                        ctk.CTkLabel(self.frame_tabla, text=t).grid(row=fila, column=0, padx=5, pady=2)
                        ctk.CTkLabel(self.frame_tabla, text=usuario.get("rut", "")).grid(row=fila, column=1, padx=5, pady=2)
                        ctk.CTkLabel(self.frame_tabla, text=usuario.get("nombre", "")).grid(row=fila, column=2, padx=5, pady=2)
                        fila += 1
                else:
                    messagebox.showwarning("Error", f"No se pudo obtener usuarios de tipo {t}: {res.status_code}")
            except Exception as e:
                messagebox.showerror("Error", f"Fallo al conectar con el servidor para tipo {t}:\n{e}")

    def eliminar(self):
        rut = self.rut_entry.get().strip()
        tipo = self.tipo_usuario.get().strip()

        if not rut or not tipo or tipo == "todos":
            messagebox.showerror("Error", "Debes especificar un tipo de usuario válido y un RUT")
            return

        try:
            response = requests.delete(f"{API_URL}/admin/eliminar/{tipo}/{rut}")
            if response.status_code == 200:
                messagebox.showinfo("Éxito", "Usuario eliminado correctamente")
                self.rut_entry.delete(0, 'end')
                self.cargar_usuarios(tipo)
            else:
                detalle = response.json().get("detail", "No se pudo eliminar el usuario")
                messagebox.showerror("Error", f"Error: {detalle}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo conectar con el servidor:\n{e}")



    def actualizar(self):
        rut = self.rut_entry.get().strip()
        tipo = self.tipo_usuario.get().strip()

        if not rut or tipo == "todos":
            messagebox.showerror("Error", "Debes especificar un RUT y un tipo de usuario válido.")
            return

        nuevos_datos = {}

        for campo, entry in self.crear_entries.items():
            valor = entry.get().strip()
            if valor:
                if campo == "edad":
                    try:
                        valor = int(valor)
                    except ValueError:
                        messagebox.showerror("Error", "Edad debe ser un número.")
                        return
            nuevos_datos[campo] = valor

        if tipo != "veterinario":
            nuevos_datos.pop("especializacion", None)

        if not nuevos_datos:
            messagebox.showwarning("Advertencia", "No se ingresaron datos nuevos para actualizar.")
            return

        try:
            response = requests.put(f"{API_URL}/admin/actualizar/{tipo}/{rut}", json=nuevos_datos)
            if response.status_code == 200:
                messagebox.showinfo("Éxito", "Usuario actualizado correctamente.")
                self.cargar_usuarios(tipo)

                # Limpiar campos del formulario
                self.rut_entry.delete(0, 'end')
                for entry in self.crear_entries.values():
                    entry.delete(0, 'end')

            else:
                detalle = response.json().get("detail", "No se pudo actualizar el usuario.")
                messagebox.showerror("Error", f"Error: {detalle}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo conectar con el servidor:\n{e}")

    def crear(self):
        tipo = self.tipo_crear.get()
        datos = {}

        # Recolectar datos del formulario
        for campo, entry in self.crear_entries.items():
            valor = entry.get()
            if not valor and campo in ["rut", "nombre", "apellido", "edad", "email", "contrasena"]:
                messagebox.showerror("error", f"El campo '{campo}' es obligatorio")
                return
            if campo == "edad":
                try:
                    valor = int(valor)
                except ValueError:
                    messagebox.showerror("error", "Edad debe ser un número")
                    return
            datos[campo] = valor

    # Quitar especialización si no es veterinario
        if tipo != "veterinario":
            datos.pop("especializacion", None)

    # Agregar el tipo al payload
        datos["tipo"] = tipo

        try:
            response = requests.post("http://127.0.0.1:8000/admin/crear", json=datos)
            if response.status_code == 200:
                messagebox.showinfo("éxito", "Usuario creado exitosamente")
                self.cargar_usuarios("todos")
            else:
                detalle = response.json().get("detail", "No se pudo crear el usuario")
                messagebox.showerror("error", f"Error: {detalle}")
        except Exception as e:
            messagebox.showerror("error", f"No se pudo conectar con el servidor:\n{e}")

