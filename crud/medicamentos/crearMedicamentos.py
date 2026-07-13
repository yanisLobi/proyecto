import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry


class CrearMedicamentos:
    def __init__(self, parent):
        #me queda la duda de que es parent
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
    
        tk.Label(self.frame, text="Nombre comercial").pack(pady=5)
        self.me_nombre_comercial = tk.Entry(self.frame, width=30)
        self.me_nombre_comercial.pack(pady=5)
        
        
        tk.Label(self.frame, text="Forma framecéutica").pack(pady=5)
        us_tipo_usuarios = tk.StringVar(value="ninguno")
        tk.Radiobutton(self.frame, text="Sólidas", variable=us_tipo_usuarios, value="Sólidas").pack()
        tk.Radiobutton(self.frame, text="Semisólidas", variable=us_tipo_usuarios, value="Semisólidas").pack()
        tk.Radiobutton(self.frame, text="Líquidas", variable=us_tipo_usuarios, value="Líquidas").pack()
        tk.Radiobutton(self.frame, text="Inhalables", variable=us_tipo_usuarios, value="Inhalables").pack()
        
        tk.Label(self.frame, text="Concentración").pack(pady=5)
        self.me_concentracion = tk.Entry(self.frame, width=30)
        self.me_concentracion.pack(pady=5)
        
        tk.Label(self.frame, text="Fecha de caducidad").pack(pady=5)
        self.me_fecha_caducidad = DateEntry(self.frame, year= 2026)
        self.me_fecha_caducidad.pack(pady=5)
        
        tk.Label(self.frame, text="Descripción")
        me_descripcion = tk.Text(self.frame, height=4, width=40)
        me_descripcion.pack(pady=5)
        
        
        
        
        
        
        