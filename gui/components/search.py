import customtkinter as ctk

class SearchBar(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self._create_widgets()
    
    def _create_widgets(self):
        self.entry = ctk.CTkEntry(self, width=300)
        self.btn = ctk.CTkButton(self, text="Buscar", width=80)
        
        self.entry.pack(side="left", padx=5)
        self.btn.pack(side="left")