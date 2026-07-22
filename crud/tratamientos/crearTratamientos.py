import tkinter as tk
import ttkbootstrap as ttkb
from tkinter import messagebox
from tkcalendar import DateEntry
from tkinter import ttk
from tkcalendar import DateEntry
from herramientas import navegar_a_pagina, limpiar_frame, insertar_registro, obtener_valores, obtener_valores_usuarios


class CrearTratamientos:
    def __init__(self, parent=None, titulo="Crear", tipo_usuario=None):
        #me queda la duda de que es parent
        self.frame = ttkb.Frame(parent)
        self.frame.pack(fill="both", expand=True)
        self.tabla = 'tratamientos'
        self.tipo_usuario = tipo_usuario
        self.etiqueta = ttkb.Label(
            self.frame,
            text=f"{titulo} {self.tabla}",
            font=("Arial", 14, "bold")
        )
        self.etiqueta.pack(pady=(40, 30))
        
        valores_pacientes = obtener_valores("pacientes", "id_pa", "pa_nombre", "pa_apellidos")
        valores_doctor = obtener_valores_usuarios("id_usuarios", "us_nombre", "us_apellidos", "Doctor")
        valores_enfermera = obtener_valores_usuarios("id_usuarios", "us_nombre", "us_apellidos", "Enfermera")

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
        self.tr_nombre = ttkb.Entry(form_frame, width=30)
        self.tr_nombre.grid(row=0, column=1, sticky="ew", pady=(0, 16))

        ttkb.Label(form_frame, text="Paciente").grid(row=0, column=2, sticky="w", padx=(20, 10), pady=(0, 16))
        self.id_paciente = ttk.Combobox(form_frame, values= valores_pacientes)
        self.id_paciente.current(0)
        self.id_paciente.grid(row=0, column=3, sticky="ew", pady=(0, 16))

        ttkb.Label(form_frame, text="Doctor").grid(row=1, column=0, sticky="w", padx=(0, 10), pady=(0, 16))
        self.id_doctor = ttk.Combobox(form_frame, values= valores_doctor)
        self.id_doctor.current(0)
        self.id_doctor.grid(row=1, column=1, sticky="ew", pady=(0, 16))

        ttkb.Label(form_frame, text="Enfermera").grid(row=1, column=0, sticky="w", padx=(0, 10), pady=(0, 16))
        self.id_enfermera = ttk.Combobox(form_frame, values= valores_enfermera)
        self.id_enfermera.current(0)
        self.id_enfermera.grid(row=1, column=1, sticky="ew", pady=(0, 16))
        
        ttkb.Label(form_frame, text="Fecha de inicio").grid(row=1, column=2, sticky="w", padx=(20, 10), pady=(0, 16))
        self.tr_fecha_inicio = DateEntry(form_frame, year= 2026)
        self.tr_fecha_inicio.grid(row=1, column=3, sticky="w", pady=(0, 16))

        ttkb.Label(form_frame, text="Fecha de terminación").grid(row=2, column=0, sticky="w", padx=(0, 10), pady=(0, 16))
        self.tr_fecha_final = DateEntry(form_frame, year= 2026)
        self.tr_fecha_final.grid(row=2, column=1, sticky="w", pady=(0, 16))

        ttkb.Label(form_frame, text="Descripción").grid(row=3, column=0, sticky="w", padx=(0, 10), pady=(0, 16))
        self.tr_descripcion = ttkb.Entry(form_frame, width=30)
        self.tr_descripcion.grid(row=3, column=1, columnspan=3, sticky="ew", pady=(0, 16))
        
        
        
    def limpiar(self):
        limpiar_frame(self.frame)
    
    def ir_lista(self):
        navegar_a_pagina(self.frame, f"Lista {self.tabla}", tipo_usuario = self.tipo_usuario)
        
    def guardar_valores(self):
        #actualizar los valores del diccionario con los valores de lo widgets
        self.nuevo_registro ={
                        'tr_nombre': '', 
                        'tr_fecha_inicio': "1980-01-01",
                        'tr_fecha_final': "1980-01-01", 
                        'tr_descripcion': '',
                        'id_paciente': "",
                        'id_usuario' : ""
                        }
        
        self.nuevo_registro["tr_nombre"] = self.tr_nombre.get()
        self.nuevo_registro["tr_fecha_inicio"] = self.tr_fecha_inicio.get_date().strftime("%Y-%m-%d")
        self.nuevo_registro["tr_fecha_final"] = self.tr_fecha_final.get_date().strftime("%Y-%m-%d")
        self.nuevo_registro["tr_descripcion"] = self.tr_descripcion.get()
        self.nuevo_registro["id_paciente"] = self.id_paciente.get().split(" ")[0]
        self.nuevo_registro["id_usuario"] = self.id_usuario.get().split(" ")[0]
        
        
       
    
    def crear_tratamientos(self):
        self.guardar_valores()
        insertar_registro(self.tabla, self.nuevo_registro)
     
        messagebox.showinfo("Crear", "Se creó correctamente el tratamiento")
        navegar_a_pagina(self.frame, f"Lista {self.tabla}", tipo_usuario=self.tipo_usuario)
        #messabox, se creó correctamente.
        #regresar a lista usuarios
    
    def guardar(self):
        self.crear_tratamientos()
    
    