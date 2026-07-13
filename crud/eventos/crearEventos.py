import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry

class CrearEventos:
    def __init__(self, parent):
        self.frame = tk.Frame(parent, bg="#f5f5f5")
        self.frame.pack(fill="both", expand=True)
    
        self.etiqueta = tk.Label(
            self.frame,
            text="Crear pacientes",
            font=("Arial", 14, "bold"),
            bg="#f5f5f5",
            fg="#2c3e50"
        )
        self.etiqueta.pack(pady=20)
    
        tk.Label(self.frame, text="Nombre").pack(pady=5)
        self.tr_nombre = tk.Entry(self.frame, width=30)
        self.nombre.pack(pady=5)
        
        tk.Label(self.frame, text="Fecha de inicio del tratamiento").pack(pady=5)
        self.tr_fecha_inicio = DateEntry(self.frame, year= 2026)
        self.tr_fecha_inicio.pack(pady=5)
        
        tk.Label(self.frame, text="Fecha de final del tratamiento").pack(pady=5)
        self.tr_fecha_final = DateEntry(self.frame, year= 2026)
        self.tr_fecha_final.pack(pady=5)
        
        tk.Label(self.frame, text="Descripción")
        tr_descripcion = tk.Text(self.frame, height=4, width=40)
        tr_descripcion.pack(pady=5)
        