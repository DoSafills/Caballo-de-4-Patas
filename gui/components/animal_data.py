import customtkinter as ctk

class AnimalDataSection(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, width=980, height=370)
        self.frame_datos_animal = ctk.CTkFrame(self)
        self.frame_datos_animal.pack(fill="both", expand=True, padx=10, pady=10)
        self.create_widgets()

    def create_widgets(self):
        ctk.CTkLabel(self.frame_datos_animal, text="Nombre:").grid(row=0, column=0, sticky='w')
        self.nombre_entry = ctk.CTkEntry(self.frame_datos_animal)
        self.nombre_entry.grid(row=0, column=1)
        
        ctk.CTkLabel(self.frame_datos_animal, text="Peso:").grid(row=1, column=0, sticky='w')
        self.peso_entry = ctk.CTkEntry(self.frame_datos_animal)
        self.peso_entry.grid(row=1, column=1)
        
        ctk.CTkLabel(self.frame_datos_animal, text="Edad").grid(row=2, column=0, sticky='w')
        self.edad_entry = ctk.CTkEntry(self.frame_datos_animal)
        self.edad_entry.grid(row=2, column=1)
        
        labels = ["Sexo:", "Especie:", "Carácter:", "Capa:", "Dieta:", "Altura:", "Chapa:", "Raza:", "Pelo:", "Censo:", "Hábitat:", "Ojos:"]
        opciones = [
            ["Macho", "Hembra"], ["Canino", "Felino"], ["Dócil", "Agresivo"], ["Amarilla", "Negra", "Blanca"],
            ["Casera y pienso", "Solo pienso"], ["Bajo", "Medio", "Alto"], [], ["Mestizo", "Pura raza"],
            ["Corto", "Largo"], [], ["Casa", "Exterior"], ["Marrones", "Azules", "Verdes"]
        ]
        
        for i in range(6):
            ctk.CTkLabel(self.frame_datos_animal, text=labels[i]).grid(row=i+3, column=0, sticky='w', padx=5, pady=2)
            ctk.CTkComboBox(self.frame_datos_animal, values=opciones[i]).grid(row=i+3, column=1, padx=5, pady=2)
        
        for i in range(6, 12):
            ctk.CTkLabel(self.frame_datos_animal, text=labels[i]).grid(row=i-5+3, column=2, sticky='w', padx=5, pady=2)
            ctk.CTkComboBox(self.frame_datos_animal, values=opciones[i]).grid(row=i-5+3, column=3, padx=5, pady=2)
        
        ver_ficha_button = ctk.CTkButton(self.frame_datos_animal, text="Ver ficha completa de la mascota")
        ver_ficha_button.grid(row=9, column=1, columnspan=2, pady=10)
        
        ctk.CTkButton(self.frame_datos_animal, text="Guardar").grid(row=10, column=1, columnspan=2, pady=10)
