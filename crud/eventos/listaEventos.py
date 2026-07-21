import tkinter as tk
import ttkbootstrap as ttkb
class ListaEventos:
    def __init__(self, parent):
        self.frame = ttkb.Frame(parent)
        self.frame.pack(fill="both", expand=True)

        self.etiqueta = ttkb.Label(
            self.frame,
            text="Lista de pacientes",
            font=("Arial", 14, "bold")
        )
        self.etiqueta.pack(pady=20)