import customtkinter as ctk
import sqlite3

class VeterinariaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Veterinario")
        self.root.geometry("1800x900")

        self.db_path = "local_database.db"  # Ruta a la base de datos

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

    def conectar_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        return conn, cursor

    def filtrar_animales(self):
        criterio = self.criterio_busqueda.get()
        valor = self.entry_busqueda.get().strip().lower()
        self.text_resultados.delete("1.0", "end")  # Limpiar resultados

        if not valor:
            self.text_resultados.insert("end", "Ingrese un criterio de búsqueda.")
            return

        conn, cursor = self.conectar_db()

        if criterio == "Nombre":
            query = "SELECT * FROM mascotas WHERE LOWER(nombre) LIKE ?"
            cursor.execute(query, ('%' + valor + '%',))
        elif criterio == "Chapa":
            query = "SELECT * FROM mascotas WHERE LOWER(chapa) = ?"
            cursor.execute(query, (valor,))

        resultados = cursor.fetchall()
        conn.close()

        if resultados:
            for a in resultados:
                texto = (
                    f"Chapa: {a[0]}, Nombre: {a[1]}, Raza: {a[2]}, Sexo: {a[3]}, "
                    f"Dieta: {a[4]}, Carácter: {a[5]}, Hábitat: {a[6]}, "
                    f"Edad: {a[7]} años, Peso: {a[8]} kg, Altura: {a[9]} cm, "
                    f"RUT Veterinario: {a[10]}"
                )
                self.text_resultados.insert("end", texto + "\n")
        else:
            self.text_resultados.insert("end", "No se encontraron resultados.")
    
if __name__ == "__main__":
    root = ctk.CTk()
    app = VeterinariaApp(root)
    root.mainloop()
