import customtkinter as ctk

class VeterinariaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Veterinario")
        self.root.geometry("1800x900")

        # Debe mostrar: chapa, nombre, raza, sexo, dieta, caracter, habitat,
        # edad, peso, altura, rut_veterinario

        # Datos de ejemplo de los animales, datos simulados (Borra mas tarde)
        self.animales = [
            {
                "chapa": 1, "nombre": "Max", "raza": "Labrador", "sexo": "Macho",
                "dieta": "Balanceada", "caracter": "Amigable", "habitat": "Casa",
                "edad": 5, "peso": 30, "altura": 60, "rut_veterinario": "12345678-9"
            },
            {
                "chapa": 2, "nombre": "Luna", "raza": "Golden Retriever", "sexo": "Hembra",
                "dieta": "Barf", "caracter": "Juguetona", "habitat": "Casa",
                "edad": 3, "peso": 25, "altura": 55, "rut_veterinario": "87654321-0"
            },
            {
                "chapa": 3, "nombre": "Rocky", "raza": "Bulldog", "sexo": "Macho",
                "dieta": "Pienso", "caracter": "Tranquilo", "habitat": "Departamento",
                "edad": 2, "peso": 20, "altura": 40, "rut_veterinario": "11223344-5"
            },
            {
                "chapa": 4, "nombre": "Milo", "raza": "Beagle", "sexo": "Macho",
                "dieta": "Comida casera", "caracter": "Curioso", "habitat": "Casa",
                "edad": 1, "peso": 10, "altura": 35, "rut_veterinario": "55667788-3"
            },
            {
                "chapa": 5, "nombre": "Bobby", "raza": "Pastor Alemán", "sexo": "Macho",
                "dieta": "Balanceada", "caracter": "Protector", "habitat": "Casa con patio",
                "edad": 4, "peso": 35, "altura": 65, "rut_veterinario": "99887766-2"
            }
        ]

        
        # frames de secciones /////////////////////
        self.frame_busqueda = ctk.CTkFrame(root, width=980, height=100)
        self.frame_busqueda.place(x=10, y=10)

        # resultados de busqueda
        self.frame_resultados = ctk.CTkFrame(root, width=600, height=300)
        self.frame_resultados.place(x=10, y=90)
        
        self.crear_seccion_busqueda()
        self.crear_seccion_resultados()

    def crear_seccion_busqueda(self):
        # ctk.CTkLabel(self.frame_busqueda, text="Nombre:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.entry_busqueda = ctk.CTkEntry(self.frame_busqueda, width=200, placeholder_text="Buscar")
        self.entry_busqueda.grid(row=0, column=1, padx=5, pady=5)

        # Opciones de busqueda/filtro, buscar por:
        self.criterio_busqueda = ctk.CTkComboBox(self.frame_busqueda, values=["Nombre", "Chapa"]) # Criterios de busqueda
        self.criterio_busqueda.grid(row=0, column=2, padx=5, pady=5)
        self.criterio_busqueda.set("Nombre")  # Valor predeterminado
        
        buscar_button = ctk.CTkButton(self.frame_busqueda, text="🔍", width=30, command=self.filtrar_animales)
        buscar_button.grid(row=0, column=3, padx=5, pady=5)
        
        ver_ficha_button = ctk.CTkButton(self.frame_busqueda, text="Ver ficha cliente")
        ver_ficha_button.grid(row=0, column=4, padx=5, pady=5)
    
    # Seccion de resultados
    def crear_seccion_resultados(self):
        ctk.CTkLabel(self.frame_resultados, text="Resultados:").grid(row=0, column=0, sticky='w')

        self.text_resultados = ctk.CTkTextbox(self.frame_resultados, width=500, height=200)
        self.text_resultados.grid(row=1, column=0)

    def filtrar_animales(self):
        criterio = self.criterio_busqueda.get()  # Obtener si se busca por "Nombre" o "ID"
        valor = self.entry_busqueda.get().strip().lower()
        self.text_resultados.delete("1.0", "end")  # Limpiar resultados

        filtrados = []

        # Criterio debe tener el mismo nombre que la ComboBox en las opciones

        if valor:
            if criterio == "Nombre":
                filtrados = [
                    f"Chapa: {a['chapa']}, Nombre: {a['nombre']}, Raza: {a['raza']}, Sexo: {a['sexo']}, "
                    f"Dieta: {a['dieta']}, Carácter: {a['caracter']}, Hábitat: {a['habitat']}, "
                    f"Edad: {a['edad']} años, Peso: {a['peso']} kg, Altura: {a['altura']} cm, "
                    f"RUT Veterinario: {a['rut_veterinario']}"
                    for a in self.animales if valor in a["nombre"].lower()
                ]
            elif criterio == "Chapa":
                filtrados = [
                    f"Chapa: {a['chapa']}, Nombre: {a['nombre']}, Raza: {a['raza']}, Sexo: {a['sexo']}, "
                    f"Dieta: {a['dieta']}, Carácter: {a['caracter']}, Hábitat: {a['habitat']}, "
                    f"Edad: {a['edad']} años, Peso: {a['peso']} kg, Altura: {a['altura']} cm, "
                    f"RUT Veterinario: {a['rut_veterinario']}"
                    for a in self.animales if valor == str(a["chapa"])
                ]

            if filtrados:
                for item in filtrados:
                    self.text_resultados.insert("end", item + "\n")
            else:
                self.text_resultados.insert("end", "No se encontraron resultados.")
        else:
            self.text_resultados.insert("end", "Ingrese un criterio de búsqueda.")
    
if __name__ == "__main__":
    root = ctk.CTk()
    app = VeterinariaApp(root)
    root.mainloop()
