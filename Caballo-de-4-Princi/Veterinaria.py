import customtkinter as ctk
import customtkinter as ctk
from tkinter import messagebox
from database import SessionLocal
from crud import obtener_veterinario_por_rut

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Login Veterinario")
        self.root.geometry("400x300")

        ctk.CTkLabel(root, text="RUT Veterinario:").pack(pady=10)
        self.rut_entry = ctk.CTkEntry(root)
        self.rut_entry.pack()

        ctk.CTkLabel(root, text="Contraseña:").pack(pady=10)
        self.pass_entry = ctk.CTkEntry(root, show="*")
        self.pass_entry.pack()

        ctk.CTkButton(root, text="Iniciar Sesión", command=self.login).pack(pady=20)

    def login(self):
        rut = self.rut_entry.get()
        contrasena = self.pass_entry.get()

        db = SessionLocal()
        veterinario = obtener_veterinario_por_rut(db, rut)

        if veterinario and veterinario.contrasena == contrasena:
            messagebox.showinfo("Éxito", f"Bienvenido {veterinario.nombre}")
            self.root.destroy()  # cerrar login
            main_window = ctk.CTk()  # crear ventana principal
            app = VeterinariaApp(main_window)
            main_window.mainloop()
        else:
            messagebox.showerror("Error", "rut o contraseña incorrectos")

        db.close()
        
class VeterinariaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Veterinario")
        self.root.geometry("1800x900")
        
        # frames de secciones /////////////////////
        self.frame_busqueda = ctk.CTkFrame(root, width=980, height=100)
        self.frame_busqueda.place(x=10, y=10)
        
        self.frame_datos_animal = ctk.CTkFrame(root, width=980, height=370)
        self.frame_datos_animal.place(x=10, y=300)
        
        self.frame_factura = ctk.CTkFrame(root, width=770, height=370)
        self.frame_factura.place(x=1010, y=270)
        
        self.frame_datos_aviso = ctk.CTkFrame(root, width=980, height=200)
        self.frame_datos_aviso.place(x=10, y=680)
        
        self.frame_adicion = ctk.CTkFrame(root, width=770, height=230)
        self.frame_adicion.place(x=1010, y=650)
        
        self.crear_seccion_busqueda()
      
        self.crear_seccion_datos_animal() 
        self.crear_seccion_factura()
        self.crear_seccion_avisos()
        self.crear_seccion_adicion()

    def crear_seccion_busqueda(self):
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
    
    def crear_seccion_datos_animal(self):
   

        ctk.CTkLabel(self.frame_datos_animal, text="Nombre:").grid(row=0, column=0, sticky='w')
        ctk.CTkEntry(self.frame_datos_animal).grid(row=0, column=1)
        
        ctk.CTkLabel(self.frame_datos_animal, text="Peso:").grid(row=1, column=0, sticky='w')
        ctk.CTkEntry(self.frame_datos_animal).grid(row=1, column=1)
        
        ctk.CTkLabel(self.frame_datos_animal, text="Edad").grid(row=2, column=0, sticky='w')
        ctk.CTkEntry(self.frame_datos_animal).grid(row=2, column=1)
        
        # s etiquetas y "Datos Generales"
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
        ver_ficha_button.grid(row=7, column=1, columnspan=2, pady=10)
        
        ctk.CTkButton(self.frame_datos_animal, text="Guardar").grid(row=9, column=0, columnspan=2, pady=10)
    
    def crear_seccion_factura(self):
        ctk.CTkLabel(self.frame_factura, text="Datos del animal y servicios realizados").pack()
        ctk.CTkButton(self.frame_factura, text="Generar PDF").pack(pady=10)
        
    def crear_seccion_avisos(self):
        ctk.CTkLabel(self.frame_datos_aviso, text="Avisos").pack()
        
    def crear_seccion_adicion(self):
        ctk.CTkLabel(self.frame_adicion, text="Adiccion").pack()
    
if __name__ == "__main__":
    root = ctk.CTk()
    app = VeterinariaApp(root)
    root.mainloop()