from datetime import datetime
import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from tkinter import messagebox
from herramientas import navegar_a_pagina, limpiar_frame, insertar_registro


class CrearPacientes:
    def __init__(self, parent, titulo="Crear", tipo_usuario=None):
        #me queda la duda de que es parent
        self.frame = tk.Frame(parent, bg="#f5f5f5")
        self.frame.pack(fill="both", expand=True)
        self.tabla = "pacientes"
        self.tipo_usuario = tipo_usuario
          
        self.etiqueta = tk.Label(
            self.frame,
            text=f"{titulo} {self.tabla} ",
            font=("Arial", 14, "bold"),
            bg="#f5f5f5",
            fg="#2c3e50"
        )
        self.etiqueta.pack(pady=20)
        
        tk.Button(self.frame, text="Limpiar campos", command=self.limpiar).pack(pady=10)
        tk.Button(self.frame, text="Cancelar", command=self.ir_lista).pack(pady=10)
        tk.Button(self.frame, text="Guardar", command=self.guardar).pack(pady=10)


        tk.Label(self.frame, text="Nombre").pack(pady=5)
        self.pa_nombre = tk.Entry(self.frame, width=30)
        self.pa_nombre.pack(pady=5)
        
        tk.Label(self.frame, text="Apellidos").pack(pady=5)
        self.pa_apellidos = tk.Entry(self.frame, width=30)
        self.pa_apellidos.pack(pady=5)
         
        tk.Label(self.frame, text="Fecha de nacimiento").pack(pady=5)
        self.pa_fecha_nacimiento = DateEntry(self.frame, year=2026)
        self.pa_fecha_nacimiento.pack(pady=5)
        
        tk.Label(self.frame, text="Nombre del contacto de emergencia").pack(pady=5)
        self.pa_nombre_contacto_emergencia = tk.Entry(self.frame, width=30)
        self.pa_nombre_contacto_emergencia.pack(pady=5)
        
        tk.Label(self.frame, text="Telefono del Contacto de emergencia").pack(pady=5)
        self.pa_tel_contacto_emergencia = tk.Entry(self.frame,width=30 )
        self.pa_tel_contacto_emergencia.pack(pady=5)
        
         
    def limpiar(self):
        limpiar_frame(self.frame)
    
    def ir_lista(self):
        navegar_a_pagina(self.frame, f"Lista {self.tabla}", tipo_usuario=self.tipo_usuario)
        
    def guardar_valores(self):
        #actualizar los valores del diccionario con los valores de lo widgets
        self.nuevo_registro ={
                        'pa_nombre': '',
                        'pa_apellidos': '', 
                        'pa_fecha_nacimiento': "1980-01-01", 
                        'pa_nombre_contacto_emergencia': '',
                        'pa_tel_contacto_emergencia': '',
                        }
        
        self.nuevo_registro["pa_nombre"] = self.pa_nombre.get()
        self.nuevo_registro["pa_apellidos"] = self.pa_apellidos.get()
        self.nuevo_registro["pa_fecha_nacimiento"] = self.pa_fecha_nacimiento.get_date().strftime("%Y-%m-%d")
        self.nuevo_registro["pa_nombre_contacto_emergencia"] = self.pa_nombre_contacto_emergencia.get()
        self.nuevo_registro["pa_tel_contacto_emergencia"] = self.pa_tel_contacto_emergencia.get()
        
        
    
    def crear_paciente(self):
        self.guardar_valores()
        insertar_registro(self.tabla, self.nuevo_registro)
     
        messagebox.showinfo("Crear", "Se creó correctamente el paciente")
        navegar_a_pagina(self.frame, "Lista pacientes", tipo_usuario=self.tipo_usuario)
        #messabox, se actualizo correctamente.
        #regresar a lista usuarios
    
    def guardar(self):
        self.crear_paciente()
           