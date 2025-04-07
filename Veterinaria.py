import customtkinter as ctk

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Login Veterinaria")
        self.root.geometry("400x300")

        ctk.CTkLabel(root, text="Inicio de Sesión", font=("Arial", 20)).pack(pady=20)

        ctk.CTkLabel(root, text="Usuario:").pack()
        self.entry_usuario = ctk.CTkEntry(root)
        self.entry_usuario.pack(pady=5)

        ctk.CTkLabel(root, text="Contraseña:").pack()
        self.entry_contrasena = ctk.CTkEntry(root, show="*")
        self.entry_contrasena.pack(pady=5)

        ctk.CTkButton(root, text="Ingresar", command=self.validar_login).pack(pady=20)

    def validar_login(self):
        usuario = self.entry_usuario.get()
        contrasena = self.entry_contrasena.get()

        # Simulación de verificación (esto se reemplazará por conexión a BD)
        if usuario == "admin" and contrasena == "1234":
            self.root.destroy()  # Cierra login
            main_app()           # Abre veterinaria
        else:
            ctk.CTkLabel(self.root, text="Usuario o contraseña incorrectos", text_color="red").pack()

class VeterinariaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Veterinario")
        self.root.geometry("1800x900")

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

    def abrir_inventario(self):
        ventana_inventario = ctk.CTkToplevel(self.root)
        ventana_inventario.title("Inventario")
        ventana_inventario.geometry("600x400")

        label = ctk.CTkLabel(ventana_inventario, text="Inventario", font=("Arial", 30))
        label.place(relx=0.5, rely=0.5, anchor="center")

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

        buscar_button = ctk.CTkButton(self.frame_busqueda, text="🔍", width=30, command=self.abrir_inventario)
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


def main_app():
    root = ctk.CTk()
    app = VeterinariaApp(root)
    root.mainloop()


if __name__ == "__main__":
    ctk.set_appearance_mode("light")  # o "dark"
    ctk.set_default_color_theme("blue")

    login_root = ctk.CTk()
    login = LoginApp(login_root)
    login_root.mainloop()
