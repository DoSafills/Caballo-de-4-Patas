import customtkinter as ctk
from crud import obtener_usuarios_por_tipo, eliminar_usuario, actualizar_usuario, crear_usuario
from database import SessionLocal
from tkinter import messagebox
from iterator import ColeccionUsuarios

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

        #self.nuevo_nombre = ctk.CTkEntry(izquierda, placeholder_text="nuevo nombre del usuario")
        #self.nuevo_nombre.pack(pady=5)

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

        usuarios = obtener_usuarios_por_tipo(self.db, tipo)
        coleccion = ColeccionUsuarios(usuarios)

        for fila, usuario in enumerate(coleccion, start=1):
            ctk.CTkLabel(self.frame_tabla, text=usuario.__class__.__name__).grid(row=fila, column=0, padx=5, pady=2)
            ctk.CTkLabel(self.frame_tabla, text=usuario.rut).grid(row=fila, column=1, padx=5, pady=2)
            ctk.CTkLabel(self.frame_tabla, text=getattr(usuario, "nombre", "")).grid(row=fila, column=2, padx=5, pady=2)

    def eliminar(self):
        rut = self.rut_entry.get()
        tipo = self.tipo_usuario.get()
        if eliminar_usuario(self.db, rut, tipo):
            messagebox.showinfo("exito", "usuario eliminado")
            self.cargar_usuarios(tipo)
        else:
            messagebox.showerror("error", "no se pudo eliminar")

    def actualizar(self):
        rut = self.rut_entry.get()
        tipo = self.tipo_usuario.get()
        nuevos_datos = {"nombre": "nuevo nombre"}
        if actualizar_usuario(self.db, rut, tipo, nuevos_datos):
            messagebox.showinfo("exito", "usuario actualizado")
            self.cargar_usuarios(tipo)
        else:
            messagebox.showerror("error", "no se pudo actualizar")

    def crear(self):
        tipo = self.tipo_crear.get()
        datos = {}
        for campo, entry in self.crear_entries.items():
            valor = entry.get()
            if campo == "edad":
                try:
                    valor = int(valor)
                except:
                    messagebox.showerror("error", "edad debe ser un numero")
                    return
            datos[campo] = valor

        if tipo != "veterinario":
            datos.pop("especializacion", None)

        if crear_usuario(self.db, tipo, datos):
            messagebox.showinfo("exito", "usuario creado")
            self.cargar_usuarios("todos")
        else:
            messagebox.showerror("error", "no se pudo crear")
