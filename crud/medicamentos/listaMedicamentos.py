import tkinter as tk
class ListaMedicamentos:
    def __init__(self, parent):
        self.frame = tk.Frame(parent, bg="#f5f5f5")
        self.frame.pack(fill="both", expand=True)

        self.etiqueta = tk.Label(
            self.frame,
            text="Lista de pacientes",
            font=("Arial", 14, "bold"),
            bg="#f5f5f5",
            fg="#2c3e50"
        )
        self.etiqueta.pack(pady=20)