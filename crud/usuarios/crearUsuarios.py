from datetime import datetime
import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from tkinter import messagebox
from herramientas import navegar_a_pagina, limpiar_frame, insertar_registro



class CrearUsuario:
    def __init__(self, parent, titulo="Crear", tipo_usuario=None):
        self.frame = tk.Frame(parent, bg="#f5f5f5")
        self.frame.pack(fill="both", expand=True)
        self.tabla = "usuarios"
        self.tipo_usuario = tipo_usuario
        
        self.etiqueta = tk.Label(
            self.frame,
            text=f"{titulo} {self.tabla}",
            font=("Arial", 14, "bold"),
            bg="#f5f5f5",
            fg="#2c3e50"
        )
        self.etiqueta.pack(pady=(40, 30))

        botones_frame = tk.Frame(self.frame, bg="#f5f5f5")
        botones_frame.pack(pady=(10, 35), padx=20, fill="x")
        botones_frame.grid_columnconfigure(0, weight=1)
        botones_frame.grid_columnconfigure(1, weight=1)
        botones_frame.grid_columnconfigure(2, weight=1)

        tk.Button(botones_frame, text="Cancelar", command=self.ir_lista).grid(row=0, column=0, sticky="ew", padx=6)
        tk.Button(botones_frame, text="Limpiar campos", command=self.limpiar).grid(row=0, column=1, sticky="ew", padx=6)
        tk.Button(botones_frame, text="Guardar", command=self.guardar).grid(row=0, column=2, sticky="ew", padx=6)

        form_frame = tk.Frame(self.frame, bg="#f5f5f5")
        form_frame.pack(padx=20, pady=(20, 30), fill="x")
        form_frame.grid_columnconfigure(0, weight=0)
        form_frame.grid_columnconfigure(1, weight=1)
        form_frame.grid_columnconfigure(2, weight=0)
        form_frame.grid_columnconfigure(3, weight=1)

        tk.Label(form_frame, text="Tipo de usuario", bg="#f5f5f5").grid(row=0, column=0, sticky="w", padx=(0, 10), pady=(0, 16))
        self.us_tipo_usuario = tk.StringVar(value="ninguno")
        self.combo_tipo_usuario = ttk.Combobox(
            form_frame,
            textvariable=self.us_tipo_usuario,
            state="readonly",
            width=27,
            values=["Administrador", "Doctor", "Enfermera"]
        )
        self.combo_tipo_usuario.grid(row=0, column=1, sticky="ew", pady=(0, 16))

        tk.Label(form_frame, text="Correo electrónico", bg="#f5f5f5").grid(row=0, column=2, sticky="w", padx=(20, 10), pady=(0, 16))
        self.us_correo_electronico = tk.Entry(form_frame, width=30)
        self.us_correo_electronico.grid(row=0, column=3, sticky="ew", pady=(0, 16))

        tk.Label(form_frame, text="Nombre", bg="#f5f5f5").grid(row=1, column=0, sticky="w", padx=(0, 10), pady=(0, 16))
        self.us_nombre = tk.Entry(form_frame, width=30)
        self.us_nombre.grid(row=1, column=1, sticky="ew", pady=(0, 16))

        tk.Label(form_frame, text="Contraseña", bg="#f5f5f5").grid(row=1, column=2, sticky="w", padx=(20, 10), pady=(0, 16))
        self.us_contra = tk.Entry(form_frame, width=30)
        self.us_contra.grid(row=1, column=3, sticky="ew", pady=(0, 16))

        tk.Label(form_frame, text="Apellidos", bg="#f5f5f5").grid(row=2, column=0, sticky="w", padx=(0, 10), pady=(0, 16))
        self.us_apellidos = tk.Entry(form_frame, width=30)
        self.us_apellidos.grid(row=2, column=1, sticky="ew", pady=(0, 16))

        tk.Label(form_frame, text="Teléfono", bg="#f5f5f5").grid(row=2, column=2, sticky="w", padx=(20, 10), pady=(0, 16))
        self.us_telefono = tk.Entry(form_frame, width=30)
        self.us_telefono.grid(row=2, column=3, sticky="ew", pady=(0, 16))

        tk.Label(form_frame, text="Fecha de nacimiento", bg="#f5f5f5").grid(row=3, column=0, sticky="w", padx=(0, 10), pady=(0, 16))
        self.us_fecha_nacimiento = DateEntry(form_frame, year= 2026)
        self.us_fecha_nacimiento.grid(row=3, column=1, sticky="w", pady=(0, 16))

        tk.Label(form_frame, text="Dirección", bg="#f5f5f5").grid(row=3, column=2, sticky="w", padx=(20, 10), pady=(0, 16))
        self.us_direccion = tk.Entry(form_frame, width=30)
        self.us_direccion.grid(row=3, column=3, sticky="ew", pady=(0, 16))

        tk.Label(form_frame, text="Especialidad", bg="#f5f5f5").grid(row=4, column=0, sticky="w", padx=(0, 10), pady=(0, 16))
        self.us_especialidad = tk.StringVar(value="ninguno")
        self.combo_especialidad = ttk.Combobox(
            form_frame,
            textvariable=self.us_especialidad,
            state="readonly",
            width=27,
            values=["Geriatría", "Médico General"]
        )
        self.combo_especialidad.grid(row=4, column=1, sticky="ew", pady=(0, 16))
        
     
        
    def limpiar(self):
        limpiar_frame(self.frame)
    
    def ir_lista(self):
        navegar_a_pagina(self.frame, f"Lista {self.tabla}", tipo_usuario=self.tipo_usuario)
        
    def guardar_valores(self):
        #actualizar los valores del diccionario con los valores de lo widgets
        self.nuevo_registro ={
                        'us_tipo_usuario': '',
                        'us_nombre': '', 
                        'us_apellidos': '', 
                        'us_fecha_nacimiento': "1980-01-01", 
                        'us_contraseña': '',
                        'us_telefono': '',
                        'us_correo_electronico': '',
                        'us_direccion': '',
                        'us_especialidad': ''}
        
        self.nuevo_registro["us_tipo_usuario"] = self.us_tipo_usuario.get()
        self.nuevo_registro["us_nombre"] = self.us_nombre.get()
        self.nuevo_registro["us_apellidos"] = self.us_apellidos.get()
        self.nuevo_registro["us_fecha_nacimiento"] = self.us_fecha_nacimiento.get_date().strftime("%Y-%m-%d")
        self.nuevo_registro["us_contraseña"] = self.us_contra.get()
        self.nuevo_registro["us_telefono"] = self.us_telefono.get() 
        self.nuevo_registro["us_correo_electronico"] = self.us_correo_electronico.get() 
        self.nuevo_registro["us_direccion"] = self.us_direccion.get() 
        self.nuevo_registro["us_especialidad"] = self.us_especialidad.get()      
        
    
    def crear_usuario(self):
        self.guardar_valores()
        insertar_registro(self.tabla, self.nuevo_registro)
     
        messagebox.showinfo("Crear", "Se creó correctamente el usuario")
        navegar_a_pagina(self.frame, "Lista usuarios", tipo_usuario=self.tipo_usuario)
        #messabox, se actualizo correctamente.
        #regresar a lista usuarios
    
    def guardar(self):
        self.crear_usuario()
           
    
          
        
        
        
        
            
            
        
        
        
        
        
        
