import customtkinter as ctk
from tkinter import messagebox
from database import SessionLocal
from crud import crear_admin, crear_veterinario, crear_recepcionista, obtener_todos_los_usuarios

class AdminRegisterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Panel Administrador - Registro de Usuarios")
        self.root.geometry("600x700")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Título
        ctk.CTkLabel(root, text="Registro de Nuevo Usuario", font=("Arial", 22)).pack(pady=20)

        # Formulario
        self.entry_rut = ctk.CTkEntry(root, placeholder_text="RUT")
        self.entry_rut.pack(pady=5)

        self.entry_nombre = ctk.CTkEntry(root, placeholder_text="Nombre")
        self.entry_nombre.pack(pady=5)

        self.entry_apellido = ctk.CTkEntry(root, placeholder_text="Apellido")
        self.entry_apellido.pack(pady=5)

        self.entry_edad = ctk.CTkEntry(root, placeholder_text="Edad")
        self.entry_edad.pack(pady=5)

        self.entry_email = ctk.CTkEntry(root, placeholder_text="Email")
        self.entry_email.pack(pady=5)

        self.entry_contrasena = ctk.CTkEntry(root, placeholder_text="Contraseña", show="*")
        self.entry_contrasena.pack(pady=5)

        self.combobox_rol = ctk.CTkComboBox(root, values=["admin", "veterinario", "recepcionista"])
        self.combobox_rol.pack(pady=10)

        # Botones
        ctk.CTkButton(root, text="Crear Usuario", command=self.crear_usuario).pack(pady=10)
        ctk.CTkButton(root, text="Actualizar Lista de Usuarios", command=self.listar_usuarios).pack(pady=5)

        # Lista de usuarios
        ctk.CTkLabel(root, text="Usuarios Registrados", font=("Arial", 16)).pack(pady=10)
        self.textbox_usuarios = ctk.CTkTextbox(root, width=500, height=250)
        self.textbox_usuarios.pack(pady=10)

        self.listar_usuarios()

    def validar_rut(self, rut: str) -> bool:
        return rut.strip() != "" and len(rut) >= 8

    def crear_usuario(self):
        db = SessionLocal()
        rut = self.entry_rut.get().strip()
        nombre = self.entry_nombre.get().strip()
        apellido = self.entry_apellido.get().strip()
        edad = self.entry_edad.get().strip()
        email = self.entry_email.get().strip()
        contrasena = self.entry_contrasena.get().strip()
        rol = self.combobox_rol.get()

        if not self.validar_rut(rut):
            messagebox.showerror("Error", "RUT no válido.")
            return

        if not edad.isdigit():
            messagebox.showerror("Error", "Edad debe ser un número.")
            return

        try:
            edad = int(edad)

            if rol == "admin":
                crear_admin(db, {
                    "rut": rut, "nombre": nombre, "apellido": apellido, "edad": edad,
                    "email": email, "tipo": "admin", "id_admin": None, "contrasena": contrasena
                })
            elif rol == "veterinario":
                crear_veterinario(db, {
                    "rut": rut, "nombre": nombre, "apellido": apellido, "edad": edad,
                    "email": email, "tipo": "veterinario", "id_vet": None,
                    "especializacion": "General", "contrasena": contrasena
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
            self.listar_usuarios()

        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")
        finally:
            db.close()

    def listar_usuarios(self):
        db = SessionLocal()
        try:
            usuarios = obtener_todos_los_usuarios(db)
            self.textbox_usuarios.delete("1.0", "end")
            for u in usuarios:
                self.textbox_usuarios.insert("end", f"{u.rut} - {u.nombre} {u.apellido} - {u.tipo}\n")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron listar usuarios: {e}")
        finally:
            db.close()

if __name__ == "__main__":
    root = ctk.CTk()
    app = AdminRegisterApp(root)
    root.mainloop()
