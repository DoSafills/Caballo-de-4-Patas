import customtkinter as ctk

class SearchSection(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, width=980, height=100)
        self.create_widgets()
    
    def create_widgets(self):
        ctk.CTkLabel(self.frame_busqueda, text="Nombre:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        nombre_entry = ctk.CTkEntry(self.frame_busqueda, width=150)
        nombre_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ctk.CTkLabel(self.frame_busqueda, text="F. Nacimiento:").grid(row=0, column=2, sticky='w', padx=5, pady=5)
        nacimiento_entry = ctk.CTkEntry(self.frame_busqueda, width=100)
        nacimiento_entry.grid(row=0, column=3, padx=5, pady=5)
        
        ctk.CTkLabel(self.frame_busqueda, text="Meses:").grid(row=0, column=4, sticky='w', padx=5, pady=5)
        meses_entry = ctk.CTkEntry(self.frame_busqueda, width=50)
        meses_entry.grid(row=0, column=5, padx=5, pady=5)
        
        ctk.CTkLabel(self.frame_busqueda, text="Edad:").grid(row=0, column=6, sticky='w', padx=5, pady=5)
        edad_entry = ctk.CTkEntry(self.frame_busqueda, width=50)
        edad_entry.grid(row=0, column=7, padx=5, pady=5)
        
        ctk.CTkLabel(self.frame_busqueda, text="Cliente:").grid(row=1, column=0, sticky='w', padx=5, pady=5)
        cliente_entry = ctk.CTkEntry(self.frame_busqueda, width=100)
        cliente_entry.grid(row=1, column=1, padx=5, pady=5)
        
        buscar_button = ctk.CTkButton(self.frame_busqueda, text="🔍", width=30)
        buscar_button.grid(row=1, column=2, padx=5, pady=5)
        
        cliente_info = ctk.CTkEntry(self.frame_busqueda, width=200)
        cliente_info.grid(row=1, column=3, padx=5, pady=5)
        
        ver_ficha_button = ctk.CTkButton(self.frame_busqueda, text="Ver ficha cliente")
        ver_ficha_button.grid(row=1, column=4, padx=5, pady=5)
    