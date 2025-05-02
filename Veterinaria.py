import customtkinter as ctk
from tkinter import messagebox
from CRUD import crear_mascota, obtener_mascota_por_nombre, eliminar_mascota, actualizar_mascota, obtener_mascotas_por_id
from database import SessionLocal

class VeterinariaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gestión Veterinaria")
        self.root.geometry("600x700")

        self.db = SessionLocal()

        self.frame = ctk.CTkFrame(master=root)
        self.frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.label = ctk.CTkLabel(master=self.frame, text="Gestión de Mascotas", font=("Arial", 20))
        self.label.pack(pady=12, padx=10)

        self.entries = {}
        for campo in ['nombre', 'chapa', 'edad', 'peso', 'altura']:
            label = ctk.CTkLabel(master=self.frame, text=campo.capitalize())
            label.pack()
            entry = ctk.CTkEntry(master=self.frame)
            entry.pack()
            self.entries[campo] = entry

        self.boton_registrar = ctk.CTkButton(master=self.frame, text="Registrar Mascota", command=self.registrar_mascota)
        self.boton_registrar.pack(pady=10)

        self.boton_buscar = ctk.CTkButton(master=self.frame, text="Buscar Mascota", command=self.buscar_mascota)
        self.boton_buscar.pack(pady=10)

        self.boton_actualizar = ctk.CTkButton(master=self.frame, text="Actualizar Mascota", command=self.actualizar_mascota)
        self.boton_actualizar.pack(pady=10)

        self.boton_eliminar = ctk.CTkButton(master=self.frame, text="Eliminar Mascota", command=self.eliminar_mascota)
        self.boton_eliminar.pack(pady=10)

        self.text_resultados = ctk.CTkTextbox(master=self.frame, height=200)
        self.text_resultados.pack(pady=10)

    def registrar_mascota(self):
        datos = {campo: self.entries[campo].get() for campo in self.entries}
        if not all(datos.values()):
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        try:
            crear_mascota(self.db, datos['nombre'], datos['chapa'], int(datos['edad']), float(datos['peso']), float(datos['altura']))
            messagebox.showinfo("Éxito", "Mascota registrada")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def buscar_mascota(self):
        chapa = self.entries['chapa'].get()
        nombre = self.entries['nombre'].get()

        if chapa:
            mascota = obtener_mascotas_por_id(self.db, chapa)
            if mascota:
                self.text_resultados.delete("1.0", "end")
                self.text_resultados.insert("end", f"Nombre: {mascota.nombre}\nChapa: {mascota.id_mascota}\nEdad: {mascota.edad }\nPeso: {mascota.peso}\nAltura: {mascota.altura}\n")
            else:
                messagebox.showinfo("Sin resultados", "No se encontró la mascota")
        elif nombre:
            mascotas = obtener_mascota_por_nombre(self.db, nombre)
            if mascotas:
                self.text_resultados.delete("1.0", "end")
                for mascota in mascotas:
                    self.text_resultados.insert("end", f"{mascota.nombre} - {mascota.chapa}\n")
            else:
                messagebox.showinfo("Sin resultados", "No se encontraron mascotas con ese nombre")
        else:
            messagebox.showinfo("Advertencia", "Ingrese al menos el nombre o la chapa")

    def actualizar_mascota(self):
        datos = {campo: self.entries[campo].get() for campo in self.entries}
        if not all(datos.values()):
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        try:
            mascota = actualizar_mascota(self.db, datos['chapa'], datos['nombre'], int(datos['edad']), float(datos['peso']), float(datos['altura']))
            if mascota:
                messagebox.showinfo("Éxito", "Mascota actualizada")
            else:
                messagebox.showinfo("Sin resultados", "No se encontró la mascota")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def eliminar_mascota(self):
        chapa = self.entries['chapa'].get()
        if not chapa:
            messagebox.showerror("Error", "Ingrese la chapa de la mascota a eliminar")
            return

        try:
            exito = eliminar_mascota(self.db, chapa)
            if exito:
                messagebox.showinfo("Éxito", "Mascota eliminada")
            else:
                messagebox.showinfo("Sin resultados", "No se encontró la mascota")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def cerrar(self):
        self.db.close()

if __name__ == '__main__':
    root = ctk.CTk()
    app = VeterinariaApp(root)
    root.protocol("WM_DELETE_WINDOW", lambda: (app.cerrar(), root.destroy()))
    root.mainloop()
