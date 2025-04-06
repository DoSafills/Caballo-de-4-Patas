import customtkinter as ctk
from gui.app import VeterinariaApp

if __name__ == '__main__':
    root = ctk.CTk()
    app = VeterinariaApp(root)
    root.mainloop()