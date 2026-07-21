import tkinter as tk
import ttkbootstrap as ttkb

class ConsultarPacientes:
    def __init__(self, parent):
        self.frame = ttkb.Frame(parent)
        self.frame.pack(fill="both", expand=True)

        self.etiqueta = ttkb.Label(
            self.frame,
            text="Consultar pacientes",
            font=("Arial", 14, "bold")
        )
        self.etiqueta.pack(pady=20)
       