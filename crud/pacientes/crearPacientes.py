from datetime import datetime
import tkinter as tk
import ttkbootstrap as ttkb
from tkinter import ttk
from tkcalendar import DateEntry
from tkinter import messagebox
from herramientas import navegar_a_pagina, limpiar_frame, insertar_registro


class CrearPacientes:
    def __init__(self, parent, titulo="Crear", tipo_usuario=None):
        #me queda la duda de que es parent
        self.frame = ttkb.Frame(parent)
        self.frame.pack(fill="both", expand=True)
        self.tabla = "pacientes"
        self.tipo_usuario = tipo_usuario
          
        self.etiqueta = ttkb.Label(
            self.frame,
            text=f"{titulo} {self.tabla} ",
            font=("Arial", 14, "bold")
        )
        self.etiqueta.pack(pady=(40, 30))

        botones_frame = ttkb.Frame(self.frame)
        botones_frame.pack(pady=(10, 35), padx=20, fill="x")
        botones_frame.grid_columnconfigure(0, weight=1)
        botones_frame.grid_columnconfigure(1, weight=1)
        botones_frame.grid_columnconfigure(2, weight=1)

        ttkb.Button(
            botones_frame,
            text="Cancelar",
            command=self.ir_lista,
            bootstyle="secondary",
        ).grid(row=0, column=0, sticky="ew", padx=6)
        ttkb.Button(
            botones_frame,
            text="Limpiar campos",
            command=self.limpiar,
            bootstyle="warning",
        ).grid(row=0, column=1, sticky="ew", padx=6)
        ttkb.Button(
            botones_frame,
            text="Guardar",
            command=self.guardar,
            bootstyle="primary",
        ).grid(row=0, column=2, sticky="ew", padx=6)

        form_frame = ttkb.Frame(self.frame)
        form_frame.pack(padx=20, pady=(20, 30), fill="x")
        form_frame.grid_columnconfigure(0, weight=0)
        form_frame.grid_columnconfigure(1, weight=1)
        form_frame.grid_columnconfigure(2, weight=0)
        form_frame.grid_columnconfigure(3, weight=1)

        ttkb.Label(form_frame, text="Nombre").grid(row=0, column=0, sticky="w", padx=(0, 10), pady=(0, 16))
        self.pa_nombre = ttkb.Entry(form_frame, width=30)
        self.pa_nombre.grid(row=0, column=1, sticky="ew", pady=(0, 16))

        ttkb.Label(form_frame, text="Apellidos").grid(row=0, column=2, sticky="w", padx=(20, 10), pady=(0, 16))
        self.pa_apellidos = ttkb.Entry(form_frame, width=30)
        self.pa_apellidos.grid(row=0, column=3, sticky="ew", pady=(0, 16))

        ttkb.Label(form_frame, text="Fecha de nacimiento").grid(row=1, column=0, sticky="w", padx=(0, 10), pady=(0, 16))
        self.pa_fecha_nacimiento = DateEntry(form_frame, year=2026)
        self.pa_fecha_nacimiento.grid(row=1, column=1, sticky="w", pady=(0, 16))

        ttkb.Label(form_frame, text="Telefono del Contacto de emergencia").grid(row=1, column=2, sticky="w", padx=(20, 10), pady=(0, 16))
        self.pa_tel_contacto_emergencia = ttkb.Entry(form_frame, width=30)
        self.pa_tel_contacto_emergencia.grid(row=1, column=3, sticky="ew", pady=(0, 16))

        ttkb.Label(form_frame, text="Nombre del contacto de emergencia").grid(row=2, column=0, sticky="w", padx=(0, 10), pady=(0, 16))
        self.pa_nombre_contacto_emergencia = ttkb.Entry(form_frame, width=30)
        self.pa_nombre_contacto_emergencia.grid(row=2, column=1, columnspan=3, sticky="ew", pady=(0, 16))
        
         
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
           