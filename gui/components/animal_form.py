import customtkinter as ctk
from database.crud import AnimalCRUD

class AnimalForm(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.animal_crud = AnimalCRUD()
        self._create_widgets()

    def _create_widgets(self):
        self.nombre = ctk.CTkEntry(self, placeholder_text="Nombre")
        self.especie = ctk.CTkComboBox(self, values=["Canino", "Felino"])
        self.btn_guardar = ctk.CTkButton(self, text="Guardar", command=self._save)

        self.nombre.grid(row=0, column=0, padx=5, pady=5)
        self.especie.grid(row=0, column=1, padx=5, pady=5)
        self.btn_guardar.grid(row=1, columnspan=2, pady=10)

    def _save(self):
        nombre = self.nombre.get()
        especie = self.especie.get()
        cliente_id = 1  # Cambiar por lógica real
        self.animal_crud.create_animal(nombre, especie, cliente_id)
        print(f"Animal '{nombre}' guardado correctamente.")
