import customtkinter as ctk

class InvoiceSection(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, width=770, height=370)
        self.create_widgets()
    
    def create_widgets(self):
        ctk.CTkLabel(self, text="Datos del animal y servicios realizados").pack()
        self.btn_pdf = ctk.CTkButton(self, text="Generar PDF")
        self.btn_pdf.pack(pady=10)