import customtkinter as ctk
from database.crud import AnimalCRUD
from .components.search import SearchBar
from .components.animal_form import AnimalForm

class VeterinariaApp:
    def __init__(self, root):
        self.root = root
        self.animal_crud = AnimalCRUD()
        self._setup_ui()
    
    def _setup_ui(self):
        self.root.geometry("1200x800")
        
        # Componentes
        self.search_bar = SearchBar(self.root)
        self.animal_form = AnimalForm(self.root)
        
        # Posicionamiento
        self.search_bar.pack(pady=10)
        self.animal_form.pack(pady=20)