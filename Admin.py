import customtkinter as ctk
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
        rut = self.rut_entry.get()
        rol = self.rol_combobox.get()
        print(f"Crear usuario {rut} con rol {rol}")

    def eliminar_usuario(self):
        rut = self.rut_entry.get()
        print(f"Eliminar usuario con rut {rut}")
