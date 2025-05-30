import customtkinter as ctk
from tkinter import messagebox
from database import SessionLocal
from strategyBusqueda import BusquedaPorRut
from contextStrategy import ContextoBusqueda
from models import Admin, Veterinario, Recepcionista
from Veterinaria import VeterinariaApp
from recepcionistaApp import GestionHorasApp
from adminApp import AdminApp
import inicio

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

        db = SessionLocal()
        try:
            estrategias = [
                (Admin, AdminApp, "Administrador"),
                (Veterinario, VeterinariaApp, "Veterinario"),
                (Recepcionista, GestionHorasApp, "Recepcionista")
            ]

            for modelo, app_clase, rol in estrategias:
                estrategia = ContextoBusqueda(BusquedaPorRut(modelo))
                usuario = estrategia.buscar(db, rut)
                if usuario and usuario.contrasena == contrasena:
                    messagebox.showinfo("Éxito", f"Bienvenido {rol}")
                    self.root.destroy()
                    main_window = ctk.CTk()
                    app_clase(main_window)
                    main_window.mainloop()
                    return

            messagebox.showerror("Error", "RUT o contraseña incorrectos")

        finally:
            db.close()

if __name__ == "__main__":
    root = ctk.CTk()
    app = LoginApp(root)
    root.mainloop()