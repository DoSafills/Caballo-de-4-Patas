import customtkinter as ctk

class AdditionalSection(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, width=770, height=230)
        self.create_widgets()
    
    def create_widgets(self):
        ctk.CTkLabel(self, text="Adicción").pack()
        # Widgets adicionales aquí