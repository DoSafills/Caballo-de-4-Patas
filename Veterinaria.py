import tkinter as tk
from tkinter import ttk

class VeterinariaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Veterinario")
        self.root.geometry("1800x900")
        
        # frames de secciones /////////////////////
        
        
        self.frame_busqueda = ttk.LabelFrame(root, text="Busqueda", padding=10)
        self.frame_busqueda.place(x=10, y=10, width=980, height=280)
        
        self.frame_info = ttk.LabelFrame(root, text="Informacion", padding=10)
        self.frame_info.place(x=1010, y=10, width=440, height=250)
        
        self.frame_datos_animal = ttk.LabelFrame(root, text="Datos del Animal", padding=10)
        self.frame_datos_animal.place(x=10, y=300, width=980, height=370)
        
        self.frame_factura = ttk.LabelFrame(root, text="Generar Factura", padding=10)
        self.frame_factura.place(x=1010, y=270, width=770, height=370)
        
        self.frame_datos_aviso = ttk.LabelFrame(root, text="Avisos", padding=10)
        self.frame_datos_aviso.place(x=10, y=680, width=980, height=200)
        
        self.frame_adicion = ttk.LabelFrame(root, text="Adicionales", padding=10)
        self.frame_adicion.place(x=1010, y=650, width=770, height=230)
        
        self.crear_seccion_busqueda()
        self.crear_seccion_info()
        self.crear_seccion_datos_animal()
        self.crear_seccion_factura()
        self.crear_seccion_avisos()
        self.crear_seccion_adicion()

    def crear_seccion_busqueda(self):
        ttk.Label(self.frame_busqueda, text="Nombre:").grid(row=0, column=0, sticky='w')
        ttk.Entry(self.frame_busqueda).grid(row=0, column=1)
        
        ttk.Label(self.frame_busqueda, text="Edad:").grid(row=1, column=0, sticky='w')
        ttk.Entry(self.frame_busqueda).grid(row=1, column=1)
        
        ttk.Label(self.frame_busqueda, text="Meses:").grid(row=2, column=0, sticky='w')
        ttk.Entry(self.frame_busqueda).grid(row=2, column=1)
        
        ttk.Label(self.frame_busqueda, text="N° Cliente:").grid(row=3, column=0, sticky='w')
        ttk.Entry(self.frame_busqueda).grid(row=3, column=1)
        
        ttk.Button(self.frame_busqueda, text="Buscar").grid(row=4, column=0, columnspan=2, pady=10)
    
    def crear_seccion_info(self):
        ttk.Label(self.frame_info, text="Informacion general").pack()
    
    def crear_seccion_datos_animal(self):
        ttk.Label(self.frame_datos_animal, text="Raza:").grid(row=0, column=0, sticky='w')
        ttk.Entry(self.frame_datos_animal).grid(row=0, column=1)
        
        ttk.Label(self.frame_datos_animal, text="Peso:").grid(row=1, column=0, sticky='w')
        ttk.Entry(self.frame_datos_animal).grid(row=1, column=1)
        
        ttk.Label(self.frame_datos_animal, text="Ultima visita:").grid(row=2, column=0, sticky='w')
        ttk.Entry(self.frame_datos_animal).grid(row=2, column=1)
        
        ttk.Button(self.frame_datos_animal, text="Guardar").grid(row=3, column=0, columnspan=2, pady=10)
    
    def crear_seccion_factura(self):
        ttk.Label(self.frame_factura, text="Datos del animal y servicios realizados").pack()
        ttk.Button(self.frame_factura, text="Generar PDF").pack(pady=10)
        
    def crear_seccion_avisos(self):
        ttk.Label(self.frame_datos_aviso, text="Avisos").pack()
        
    def crear_seccion_adicion(self):
        ttk.Label(self.frame_adicion, text="Adiccion").pack()
    

if __name__ == "__main__":
    root = tk.Tk()
    app = VeterinariaApp(root)
    root.mainloop()
