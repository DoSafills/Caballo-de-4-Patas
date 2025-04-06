import customtkinter as ctk
from database.crud import AnimalCRUD
class SearchSection(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, width=980, height=100)
        self.animal_crud = AnimalCRUD()
        self.frame_busqueda = ctk.CTkFrame(self)
        self.frame_busqueda.pack(fill="both", expand=True, padx=10, pady=10)
        self.create_widgets()

    def create_widgets(self):
        ctk.CTkLabel(self.frame_busqueda, text="Nombre:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.nombre_entry = ctk.CTkEntry(self.frame_busqueda, width=150)
        self.nombre_entry.grid(row=0, column=1, padx=5, pady=5)

        ctk.CTkLabel(self.frame_busqueda, text="F. Nacimiento:").grid(row=0, column=2, sticky='w', padx=5, pady=5)
        self.nacimiento_entry = ctk.CTkEntry(self.frame_busqueda, width=100)
        self.nacimiento_entry.grid(row=0, column=3, padx=5, pady=5)

        ctk.CTkLabel(self.frame_busqueda, text="Meses:").grid(row=0, column=4, sticky='w', padx=5, pady=5)
        self.meses_entry = ctk.CTkEntry(self.frame_busqueda, width=50)
        self.meses_entry.grid(row=0, column=5, padx=5, pady=5)

        ctk.CTkLabel(self.frame_busqueda, text="Edad:").grid(row=0, column=6, sticky='w', padx=5, pady=5)
        self.edad_entry = ctk.CTkEntry(self.frame_busqueda, width=50)
        self.edad_entry.grid(row=0, column=7, padx=5, pady=5)

        ctk.CTkLabel(self.frame_busqueda, text="Cliente:").grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.cliente_entry = ctk.CTkEntry(self.frame_busqueda, width=100)
        self.cliente_entry.grid(row=1, column=1, padx=5, pady=5)

        self.buscar_button = ctk.CTkButton(self.frame_busqueda, text="🔍", width=30, command=self.buscar)
        self.buscar_button.grid(row=1, column=2, padx=5, pady=5)

        self.cliente_info = ctk.CTkEntry(self.frame_busqueda, width=200)
        self.cliente_info.grid(row=1, column=3, padx=5, pady=5)

        self.ver_ficha_button = ctk.CTkButton(self.frame_busqueda, text="Ver ficha cliente")
        self.ver_ficha_button.grid(row=1, column=4, padx=5, pady=5)

    def buscar(self):
        nombre = self.nombre_entry.get()
        resultados = self.animal_crud.db.cursor.execute(
            "SELECT animales.id, animales.nombre, animales.especie, clientes.nombre FROM animales INNER JOIN clientes ON animales.cliente_id = clientes.id WHERE animales.nombre LIKE ?",
            ('%' + nombre + '%',)
        ).fetchall()

        if resultados:
            resultado = resultados[0]  # tomando el primero encontrado como ejemplo
            animal_id, animal_nombre, animal_especie, cliente_nombre = resultado

            self.nombre_entry.delete(0, ctk.END)
            self.nombre_entry.insert(0, animal_nombre)

            self.cliente_info.delete(0, ctk.END)
            self.cliente_info.insert(0, cliente_nombre)

            print(f"Animal encontrado: {animal_nombre}, especie: {animal_especie}, Cliente: {cliente_nombre}")
        else:
            print("No se encontraron resultados.")
            self.cliente_info.delete(0, ctk.END)
            self.cliente_info.insert(0, "No encontrado")
