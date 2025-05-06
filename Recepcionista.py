import customtkinter as ctk
from Persona import Persona

class Recepcionista(Persona):
    def __init__(self, id_recepcionista, contrasena, rut, nombre, apellido):
        super().__init__(rut, nombre, apellido)
        self.id_recepcionista = id_recepcionista
        self.contrasena = contrasena

class RecepcionistaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Panel Recepcionista")
        self.root.geometry("600x400")
        self.root.configure(bg="gray")
        ctk.CTkLabel(self.root, text="Bienvenido al Panel de Recepcionista", font=("Arial", 20)).pack(pady=40)
