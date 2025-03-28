import customtkinter as ctk

class AnimalForm(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self._create_widgets()
    
    def _create_widgets(self):
        # Campos del formulario
        self.nombre = ctk.CTkEntry(self, placeholder_text="Nombre")
        self.especie = ctk.CTkComboBox(self, values=["Canino", "Felino"])
        self.btn_guardar = ctk.CTkButton(self, text="Guardar", command=self._save)
        
        # Grid layout
        self.nombre.grid(row=0, column=0, padx=5, pady=5)
        self.especie.grid(row=0, column=1, padx=5, pady=5)
        self.btn_guardar.grid(row=1, columnspan=2, pady=10)
    
    def _save(self):
        print(f"Guardando: {self.nombre.get()}, {self.especie.get()}")
        # Aquí llamarías a AnimalCRUD().create_animal(...)