import tkinter as tk
import ttkbootstrap as ttkb
from tkinter import messagebox
from tkcalendar import DateEntry

class CrearEventos:
    def __init__(self, parent):
        self.frame = ttkb.Frame(parent)
        self.frame.pack(fill="both", expand=True)
    
        self.etiqueta = ttkb.Label(
            self.frame,
            text="Crear pacientes",
            font=("Arial", 14, "bold")
        )
        self.etiqueta.pack(pady=(40, 30))

        form_frame = ttkb.Frame(self.frame)
        form_frame.pack(padx=20, pady=(20, 30), fill="x")
        form_frame.grid_columnconfigure(0, weight=0)
        form_frame.grid_columnconfigure(1, weight=1)
        form_frame.grid_columnconfigure(2, weight=0)
        form_frame.grid_columnconfigure(3, weight=1)

        ttkb.Label(form_frame, text="Nombre").grid(row=0, column=0, sticky="w", padx=(0, 10), pady=(0, 16))
        self.tr_nombre = ttkb.Entry(form_frame, width=30)
        self.tr_nombre.grid(row=0, column=1, sticky="ew", pady=(0, 16))

        ttkb.Label(form_frame, text="Fecha de inicio del tratamiento").grid(row=0, column=2, sticky="w", padx=(20, 10), pady=(0, 16))
        self.tr_fecha_inicio = DateEntry(form_frame, year= 2026)
        self.tr_fecha_inicio.grid(row=0, column=3, sticky="w", pady=(0, 16))

        ttkb.Label(form_frame, text="Fecha de final del tratamiento").grid(row=1, column=0, sticky="w", padx=(0, 10), pady=(0, 16))
        self.tr_fecha_final = DateEntry(form_frame, year= 2026)
        self.tr_fecha_final.grid(row=1, column=1, sticky="w", pady=(0, 16))

        ttkb.Label(form_frame, text="Descripción").grid(row=2, column=0, sticky="nw", padx=(0, 10), pady=(0, 16))
        tr_descripcion = tk.Text(form_frame, height=4, width=40)
        tr_descripcion.grid(row=2, column=1, columnspan=3, sticky="ew", pady=(0, 16))
        