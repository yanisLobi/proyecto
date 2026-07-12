import tkinter as tk

class CrearUsuario:
    def __init__(self, parent):
        self.frame = tk.Frame(parent, bg="#f5f5f5")
        self.frame.pack(fill="both", expand=True)

        self.etiqueta = tk.Label(
            self.frame,
            text="Crear usuario",
            font=("Arial", 14, "bold"),
            bg="#f5f5f5",
            fg="#2c3e50"
        )
        self.etiqueta.pack(pady=20)
       
  
