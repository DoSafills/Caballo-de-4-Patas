import customtkinter as ctk
from tkinter import messagebox
from database import SessionLocal
from crud import crear_admin, eliminar_admin_por_rut,crear_veterinario, eliminar_veterinario_por_rut,crear_recepcionista, eliminar_recepcionista_por_rut
#a
class AdminApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Panel Administrador")
        self.root.geometry("800x500")

        ctk.CTkLabel(self.root, text="Administrador - Gestión de Usuarios", font=("Arial", 20)).pack(pady=20)

        self.rut_entry = ctk.CTkEntry(self.root, placeholder_text="RUT")
        self.rut_entry.pack(pady=5)

        self.nombre_entry = ctk.CTkEntry(self.root, placeholder_text="Nombre")
        self.nombre_entry.pack(pady=5)

        self.apellido_entry = ctk.CTkEntry(self.root, placeholder_text="Apellido")
        self.apellido_entry.pack(pady=5)

        self.edad_entry = ctk.CTkEntry(self.root, placeholder_text="Edad")
        self.edad_entry.pack(pady=5)

        self.email_entry = ctk.CTkEntry(self.root, placeholder_text="Email")
        self.email_entry.pack(pady=5)

        self.contrasena_entry = ctk.CTkEntry(self.root, placeholder_text="Contraseña", show="*")
        self.contrasena_entry.pack(pady=5)

        self.rol_combobox = ctk.CTkComboBox(self.root, values=["admin", "veterinario", "recepcionista"])
        self.rol_combobox.pack(pady=10)

        ctk.CTkButton(self.root, text="Crear Usuario", command=self.crear_usuario).pack(pady=5)
        ctk.CTkButton(self.root, text="Eliminar Usuario", command=self.eliminar_usuario).pack(pady=5)

    def crear_usuario(self):
        db = SessionLocal()
        rut = self.rut_entry.get()
        nombre = self.nombre_entry.get()
        apellido = self.apellido_entry.get()
        edad = int(self.edad_entry.get())
        email = self.email_entry.get()
        contrasena = self.contrasena_entry.get()
        rol = self.rol_combobox.get()

        try:
            if rol == "admin":
                crear_admin(db, {
                    "rut": rut, "nombre": nombre, "apellido": apellido, "edad": edad,
                    "email": email, "tipo": "admin", "id_admin": None, "contrasena": contrasena
                })
            elif rol == "veterinario":
                crear_veterinario(db, {
                    "rut": rut, "nombre": nombre, "apellido": apellido, "edad": edad,
                    "email": email, "tipo": "veterinario", "id_vet": None, "especializacion": "General",
                    "contrasena": contrasena
                })
            elif rol == "recepcionista":
                crear_recepcionista(db, {
                    "rut": rut, "nombre": nombre, "apellido": apellido, "edad": edad,
                    "email": email, "tipo": "recepcionista", "id_recepcionista": None,
                    "contrasena": contrasena
                })
            else:
                messagebox.showerror("Error", "Rol no válido.")
                return

            messagebox.showinfo("Éxito", f"{rol.capitalize()} creado correctamente.")

        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")
        finally:
            db.close()

    def eliminar_usuario(self):
        db = SessionLocal()
        rut = self.rut_entry.get()
        rol = self.rol_combobox.get()

        try:
            if rol == "admin":
                exito = eliminar_admin_por_rut(db, rut)
            elif rol == "veterinario":
                exito = eliminar_veterinario_por_rut(db, rut)
            elif rol == "recepcionista":
                exito = eliminar_recepcionista_por_rut(db, rut)
            else:
                messagebox.showerror("Error", "Rol no válido.")
                return

            if exito:
                messagebox.showinfo("Éxito", f"Usuario con RUT {rut} eliminado correctamente.")
            else:
                messagebox.showwarning("No encontrado", f"No se encontró usuario con RUT {rut}.")

        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")
        finally:
            db.close()
