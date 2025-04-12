import customtkinter as ctk
from tkinter import messagebox
from database import SessionLocal
from crud import obtener_veterinario_por_rut
from Veterinaria import VeterinariaApp

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Login Veterinario")
        self.root.geometry("400x300")

        ctk.CTkLabel(root, text="RUT Veterinario:").pack(pady=10)
        self.rut_entry = ctk.CTkEntry(root)
        self.rut_entry.pack()

        ctk.CTkLabel(root, text="Contraseña:").pack(pady=10)
        self.pass_entry = ctk.CTkEntry(root, show="*")
        self.pass_entry.pack()

        ctk.CTkButton(root, text="Iniciar Sesión", command=self.login).pack(pady=20)

    def login(self):
        rut = self.rut_entry.get()
        contrasena = self.pass_entry.get()

        db = SessionLocal()
        veterinario = obtener_veterinario_por_rut(db, rut)

        if veterinario and veterinario.contrasena == contrasena:
            messagebox.showinfo("Éxito", f"Bienvenido {veterinario.nombre}")
            self.root.destroy()  # cerrar login
            main_window = ctk.CTk()  # crear ventana principal
            app = VeterinariaApp(main_window)
            main_window.mainloop()
        else:
            messagebox.showerror("Error", "rut o contraseña incorrectos")

        db.close()

if __name__ == "__main__":
    root = ctk.CTk()
    app = LoginApp(root)
    root.mainloop()
