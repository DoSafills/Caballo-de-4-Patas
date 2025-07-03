import customtkinter as ctk
from tkinter import messagebox
import requests
from Veterinaria import VeterinariaApp
from RecepcionistaApp import GestionHorasApp
from adminApp import AdminApp


class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Login Usuario")
        self.root.geometry("400x350")

        ctk.CTkLabel(root, text="RUT Usuario:", font=ctk.CTkFont(size=14)).pack(pady=10)
        self.rut_entry = ctk.CTkEntry(root, width=250)
        self.rut_entry.pack()

        ctk.CTkLabel(root, text="Contraseña:", font=ctk.CTkFont(size=14)).pack(pady=10)
        self.pass_entry = ctk.CTkEntry(root, show="*", width=250)
        self.pass_entry.pack()

        ctk.CTkButton(root, text="Iniciar Sesión", command=self.login).pack(pady=20)

    def login(self):
        rut = self.rut_entry.get()
        contrasena = self.pass_entry.get()

        try:
            response = requests.post(
                "http://127.0.0.1:8000/auth/login",
                json={"rut": rut, "contrasena": contrasena}
            )

            if response.status_code == 200:
                data = response.json()
                rol = data["rol"]

                messagebox.showinfo("Éxito", f"Bienvenido {data['nombre']} ({rol})")
                self.root.destroy()

                ventana = ctk.CTk()
                if rol == "Administrador":
                    AdminApp(ventana)
                elif rol == "Veterinario":
                    VeterinariaApp(ventana)
                elif rol == "Recepcionista":
                    GestionHorasApp(ventana)
                else:
                    messagebox.showerror("Error", "Rol desconocido")
                    return

                ventana.mainloop()
            else:
                messagebox.showerror("Error", response.json()["detail"])

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo conectar con la API\n{str(e)}")

if __name__ == "__main__":
    root = ctk.CTk()
    app = LoginApp(root)
    root.mainloop()
