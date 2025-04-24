import customtkinter as ctk

class RecepcionistaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Panel Recepcionista")
        self.root.geometry("600x400")
        self.root.configure(bg="gray")
        ctk.CTkLabel(self.root, text="Bienvenido al Panel de Recepcionista", font=("Arial", 20)).pack(pady=40)
