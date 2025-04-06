import customtkinter as ctk
from .components.search import SearchSection
from .components.animal_data import AnimalDataSection
from .components.invoice import InvoiceSection
from .components.notices import NoticesSection
from .components.additional import AdditionalSection

class VeterinariaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Veterinario")
        self.root.geometry("1800x900")

        self.search_section = SearchSection(self.root)
        self.animal_data_section = AnimalDataSection(self.root)
        self.invoice_section = InvoiceSection(self.root)
        self.notices_section = NoticesSection(self.root)
        self.additional_section = AdditionalSection(self.root)

        self.place_sections()

    def place_sections(self):
        self.search_section.place(x=10, y=10)
        self.animal_data_section.place(x=10, y=120)
        self.invoice_section.place(x=1010, y=120)
        self.notices_section.place(x=10, y=500)
        self.additional_section.place(x=1010, y=500)

if __name__ == "__main__":
    root = ctk.CTk()
    app = VeterinariaApp(root)
    root.mainloop()
