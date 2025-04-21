import customtkinter as ctk
from tkinter import messagebox
from database import SessionLocal
from crud import crear_mascota, obtener_mascota_por_chapa, actualizar_mascota
from models import Mascota

class VeterinariaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Veterinario")
        self.root.geometry("1800x900")
        
        # Configuración de la base de datos
        self.db = SessionLocal()
        
        # Variables para almacenar datos
        self.current_mascota = None
        
        # frames de secciones
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
        
        # Diccionario para almacenar widgets de entrada
        self.entries = {}
        self.comboboxes = {}
        
        self.crear_seccion_busqueda()
        self.crear_seccion_datos_animal() 
        self.crear_seccion_factura()
        self.crear_seccion_avisos()
        self.crear_seccion_adicion()

    def crear_seccion_busqueda(self):
        ctk.CTkLabel(self.frame_busqueda, text="Nombre:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.entries['nombre_busqueda'] = ctk.CTkEntry(self.frame_busqueda, width=150)
        self.entries['nombre_busqueda'].grid(row=0, column=1, padx=5, pady=5)
        
        ctk.CTkLabel(self.frame_busqueda, text="Chapa:").grid(row=0, column=2, sticky='w', padx=5, pady=5)
        self.entries['chapa_busqueda'] = ctk.CTkEntry(self.frame_busqueda, width=100)
        self.entries['chapa_busqueda'].grid(row=0, column=3, padx=5, pady=5)
        
        buscar_button = ctk.CTkButton(self.frame_busqueda, text="🔍 Buscar", width=100, 
                                    command=self.buscar_mascota)
        buscar_button.grid(row=0, column=4, padx=5, pady=5)
        
        nueva_button = ctk.CTkButton(self.frame_busqueda, text="➕ Nueva Mascota", width=120,
                                command=self.nueva_mascota)
        nueva_button.grid(row=0, column=5, padx=5, pady=5)

    def crear_seccion_datos_animal(self):
        # Campos básicos
        ctk.CTkLabel(self.frame_datos_animal, text="Chapa:").grid(row=0, column=0, sticky='w', padx=5, pady=2)
        self.entries['chapa'] = ctk.CTkEntry(self.frame_datos_animal)
        self.entries['chapa'].grid(row=0, column=1, padx=5, pady=2)
        
        ctk.CTkLabel(self.frame_datos_animal, text="Nombre:").grid(row=1, column=0, sticky='w', padx=5, pady=2)
        self.entries['nombre'] = ctk.CTkEntry(self.frame_datos_animal)
        self.entries['nombre'].grid(row=1, column=1, padx=5, pady=2)
        
        ctk.CTkLabel(self.frame_datos_animal, text="Peso:").grid(row=2, column=0, sticky='w', padx=5, pady=2)
        self.entries['peso'] = ctk.CTkEntry(self.frame_datos_animal)
        self.entries['peso'].grid(row=2, column=1, padx=5, pady=2)
        
        ctk.CTkLabel(self.frame_datos_animal, text="Edad:").grid(row=3, column=0, sticky='w', padx=5, pady=2)
        self.entries['edad'] = ctk.CTkEntry(self.frame_datos_animal)
        self.entries['edad'].grid(row=3, column=1, padx=5, pady=2)
        
        ctk.CTkLabel(self.frame_datos_animal, text="Altura:").grid(row=4, column=0, sticky='w', padx=5, pady=2)
        self.entries['altura'] = ctk.CTkEntry(self.frame_datos_animal)
        self.entries['altura'].grid(row=4, column=1, padx=5, pady=2)
        
        # Comboboxes para opciones
        labels = ["Sexo:", "Raza:", "Carácter:", "Dieta:", "Hábitat:"]
        opciones = [
            ["Macho", "Hembra"],
            ["Mestizo", "Labrador", "Persa", "Siames", "Otro"],
            ["Dócil", "Agresivo", "Tímido", "Juguetón"],
            ["Carnívora", "Herbívora", "Omnívora", "Balanceada"],
            ["Casa", "Exterior", "Mixto"]
        ]
        keys = ['sexo', 'raza', 'caracter', 'dieta', 'habitat']
        
        for i, (label, opcion, key) in enumerate(zip(labels, opciones, keys)):
            ctk.CTkLabel(self.frame_datos_animal, text=label).grid(row=i, column=2, sticky='w', padx=5, pady=2)
            self.comboboxes[key] = ctk.CTkComboBox(self.frame_datos_animal, values=opcion)
            self.comboboxes[key].grid(row=i, column=3, padx=5, pady=2)
        
        # Botones de acción
        guardar_button = ctk.CTkButton(self.frame_datos_animal, text="Guardar", command=self.guardar_mascota)
        guardar_button.grid(row=6, column=0, columnspan=2, pady=10)
        
        eliminar_button = ctk.CTkButton(self.frame_datos_animal, text="Eliminar", fg_color="#d9534f", 
                                    command=self.eliminar_mascota)
        eliminar_button.grid(row=6, column=2, columnspan=2, pady=10)

    def buscar_mascota(self):
        chapa = self.entries['chapa_busqueda'].get()
        nombre = self.entries['nombre_busqueda'].get()
        
        if chapa:
            mascota = obtener_mascota_por_chapa(self.db, chapa)
            if mascota:
                self.mostrar_mascota(mascota)
                messagebox.showinfo("Éxito", f"Mascota encontrada: {mascota.nombre}")
            else:
                messagebox.showerror("Error", "No se encontró mascota con esa chapa")
        elif nombre:
            # Aquí podrías implementar búsqueda por nombre si lo necesitas
            messagebox.showwarning("Búsqueda", "La búsqueda por nombre no está implementada aún")
        else:
            messagebox.showwarning("Búsqueda", "Ingrese al menos un criterio de búsqueda")

    def nueva_mascota(self):
        self.current_mascota = None
        self.limpiar_campos()
        messagebox.showinfo("Nueva Mascota", "Complete los datos de la nueva mascota")

    def mostrar_mascota(self, mascota: Mascota):
        self.current_mascota = mascota
        self.entries['chapa'].delete(0, 'end')
        self.entries['chapa'].insert(0, mascota.chapa)
        self.entries['nombre'].delete(0, 'end')
        self.entries['nombre'].insert(0, mascota.nombre)
        self.entries['peso'].delete(0, 'end')
        self.entries['peso'].insert(0, mascota.peso)
        self.entries['edad'].delete(0, 'end')
        self.entries['edad'].insert(0, str(mascota.edad))
        self.entries['altura'].delete(0, 'end')
        self.entries['altura'].insert(0, mascota.altura)
        
        # Configurar comboboxes
        if mascota.sexo:
            self.comboboxes['sexo'].set(mascota.sexo)
        if mascota.raza:
            self.comboboxes['raza'].set(mascota.raza)
        if mascota.caracter:
            self.comboboxes['caracter'].set(mascota.caracter)
        if mascota.dieta:
            self.comboboxes['dieta'].set(mascota.dieta)
        if mascota.habitat:
            self.comboboxes['habitat'].set(mascota.habitat)

    def limpiar_campos(self):
        for entry in self.entries.values():
            entry.delete(0, 'end')
        for combobox in self.comboboxes.values():
            combobox.set('')

    def guardar_mascota(self):
        try:
            datos = {
                'chapa': self.entries['chapa'].get(),
                'nombre': self.entries['nombre'].get(),
                'peso': self.entries['peso'].get(),
                'edad': int(self.entries['edad'].get()),
                'altura': self.entries['altura'].get(),
                'sexo': self.comboboxes['sexo'].get(),
                'raza': self.comboboxes['raza'].get(),
                'caracter': self.comboboxes['caracter'].get(),
                'dieta': self.comboboxes['dieta'].get(),
                'habitat': self.comboboxes['habitat'].get()
            }
            
            if not datos['chapa']:
                messagebox.showerror("Error", "La chapa es obligatoria")
                return
                
            if not datos['nombre']:
                messagebox.showerror("Error", "El nombre es obligatorio")
                return
                
            if self.current_mascota:
                # Actualizar mascota existente
                mascota = actualizar_mascota(
                    self.db,
                    chapa=datos['chapa'],
                    nombre=datos['nombre'],
                    raza=datos['raza'],
                    sexo=datos['sexo'],
                    dieta=datos['dieta'],
                    caracter=datos['caracter'],
                    habitat=datos['habitat'],
                    edad=datos['edad'],
                    peso=datos['peso'],
                    altura=datos['altura']
                )
                if mascota:
                    messagebox.showinfo("Éxito", f"Mascota {mascota.nombre} actualizada correctamente")
                else:
                    messagebox.showerror("Error", "No se pudo actualizar la mascota")
            else:
                # Crear nueva mascota
                mascota = crear_mascota(
                    self.db,
                    chapa=datos['chapa'],
                    nombre=datos['nombre'],
                    raza=datos['raza'],
                    sexo=datos['sexo'],
                    dieta=datos['dieta'],
                    caracter=datos['caracter'],
                    habitat=datos['habitat'],
                    edad=datos['edad'],
                    peso=datos['peso'],
                    altura=datos['altura']
                )
                if mascota:
                    messagebox.showinfo("Éxito", f"Mascota {mascota.nombre} creada correctamente")
                    self.current_mascota = mascota
                else:
                    messagebox.showerror("Error", "No se pudo crear la mascota")
                    
        except ValueError as e:
            messagebox.showerror("Error", f"Datos inválidos: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar: {str(e)}")

    def eliminar_mascota(self):
        if not self.current_mascota:
            messagebox.showwarning("Eliminar", "No hay mascota seleccionada")
            return
            
        confirmacion = messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Está seguro que desea eliminar a {self.current_mascota.nombre}?"
        )
        
        if confirmacion:
            from crud import eliminar_mascota
            if eliminar_mascota(self.db, self.current_mascota.chapa):
                messagebox.showinfo("Éxito", "Mascota eliminada correctamente")
                self.limpiar_campos()
                self.current_mascota = None
            else:
                messagebox.showerror("Error", "No se pudo eliminar la mascota")

    def crear_seccion_factura(self):
        ctk.CTkLabel(self.frame_factura, text="Datos del animal y servicios realizados").pack()
        ctk.CTkButton(self.frame_factura, text="Generar PDF").pack(pady=10)
        
    def crear_seccion_avisos(self):
        ctk.CTkLabel(self.frame_datos_aviso, text="Avisos").pack()
        
    def crear_seccion_adicion(self):
        ctk.CTkLabel(self.frame_adicion, text="Adición").pack()
    
    def __del__(self):
        # Cerrar la conexión a la base de datos cuando se destruye la aplicación
        if hasattr(self, 'db'):
            self.db.close()

if __name__ == "__main__":
    root = ctk.CTk()
    app = VeterinariaApp(root)
    root.mainloop()