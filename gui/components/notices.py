import customtkinter as ctk

class NoticesSection(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, width=980, height=200)
        self.create_widgets()
    
    def create_widgets(self):
        ctk.CTkLabel(self, text="Avisos").pack()
        # Puedes añadir aquí un CTkTextbox para mostrar los avisos