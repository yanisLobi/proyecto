import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
from tkinter import ttk
from tkcalendar import DateEntry
from herramientas import navegar_a_pagina, limpiar_frame, insertar_registro


class CrearTratamientos:
    def __init__(self, parent, titulo="Crear"):
        #me queda la duda de que es parent
        self.frame = tk.Frame(parent, bg="#f5f5f5")
        self.frame.pack(fill="both", expand=True)
        self.tabla = 'tratamiento'
        
        self.etiqueta = tk.Label(
            self.frame,
            text=f"{titulo} {self.tabla}",
            font=("Arial", 14, "bold"),
            bg="#f5f5f5",
            fg="#2c3e50"
        )
        self.etiqueta.pack(pady=20)
        
        tk.Button(self.frame, text="Limpiar campos", command=self.limpiar).pack(pady=10)
        tk.Button(self.frame, text="Cancelar", command=self.ir_lista).pack(pady=10)
        tk.Button(self.frame, text="Guardar", command=self.guardar).pack(pady=10)
    
        tk.Label(self.frame, text="Nombre").pack(pady=5)
        self.tr_nombre = tk.Entry(self.frame, width=30)
        self.tr_nombre.pack(pady=5)
        
        tk.Label(self.frame, text="Fecha de inicio").pack(pady=5)
        self.tr_fecha_inicio = DateEntry(self.frame, year= 2026)
        self.tr_fecha_inicio.pack(pady=5)
        
        tk.Label(self.frame, text="Fecha de terminación").pack(pady=5)
        self.tr_fecha_final = DateEntry(self.frame, year= 2026)
        self.tr_fecha_final.pack(pady=5)
        
        tk.Label(self.frame, text="Descripción").pack(pady=5)
        self.tr_descripcion = tk.Text(self.frame, width=40)
        self.tr_descripcion.pack(pady=5)
        
    def limpiar(self):
        limpiar_frame(self.frame)
    
    def ir_lista(self):
        navegar_a_pagina(self.frame, f"Lista {self.tabla}")
        
    def guardar_valores(self):
        #actualizar los valores del diccionario con los valores de lo widgets
        self.nuevo_registro ={
                        'tr_nombre': '', 
                        'tr_fecha_inicio': "1980-01-01",
                        'tr_fecha_final': "1980-01-01", 
                        'tr_descripcion': ''
                        }
        
        self.nuevo_registro["tr_nombre"] = self.tr_nombre.get()
        self.nuevo_registro["tr_fecha_inicio"] = self.tr_fecha_inicio.get_date().strftime("%Y-%m-%d")
        self.nuevo_registro["tr_fecha_final"] = self.tr_fecha_final.get_date().strftime("%Y-%m-%d")
        self.nuevo_registro["tr_descripcion"] = self.tr_descripcion.get("1.0","end-1c")
       
    
    def crear_tratamientos(self):
        self.guardar_valores()
        insertar_registro(self.tabla, self.nuevo_registro)
     
        messagebox.showinfo("Crear", "Se creó correctamente el tratamiento")
        navegar_a_pagina(self.frame, f"Lista {self.tabla}")
        #messabox, se creó correctamente.
        #regresar a lista usuarios
    
    def guardar(self):
        self.crear_tratamientos()