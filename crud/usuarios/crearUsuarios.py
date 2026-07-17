from datetime import datetime
import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from tkinter import messagebox
from herramientas import navegar_a_pagina, limpiar_frame, insertar_registro



class CrearUsuario:
    def __init__(self, parent, titulo="Crear"):
        self.frame = tk.Frame(parent, bg="#f5f5f5")
        self.frame.pack(fill="both", expand=True)
        self.tabla = "usuarios"
        #crear diccionario 
        
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
        
        

        tk.Label(self.frame, text="Tipo de usuario").pack(pady=5)
        self.us_tipo_usuario = tk.StringVar(value="ninguno")
        self.combo_tipo_usuario = ttk.Combobox(
            self.frame,
            textvariable=self.us_tipo_usuario,
            state="readonly",
            width=27,
            values=["Administrador", "Doctor", "Enfermera"]
        )
        self.combo_tipo_usuario.pack(pady=5)
#agregar tipo usuario alnuevo diccionario
        tk.Label(self.frame, text="Nombre").pack(pady=5)
        self.us_nombre = tk.Entry(self.frame, width=30)
        self.us_nombre.pack(pady=5)
        
        tk.Label(self.frame, text="Apellidos").pack(pady=5)
        self.us_apellidos = tk.Entry(self.frame, width=30)
        self.us_apellidos.pack(pady=5)
        
        
        tk.Label(self.frame, text="Fecha de nacimiento").pack(pady=5)
        self.us_fecha_nacimiento = DateEntry(self.frame, year= 2026)
        self.us_fecha_nacimiento.pack(pady=5)
        
        tk.Label(self.frame, text="Contraseña").pack(pady=5)
        self.us_contra = tk.Entry(self.frame, width=30)
        self.us_contra.pack(pady=5)
        
        tk.Label(self.frame, text="Teléfono").pack(pady=5)
        self.us_telefono = tk.Entry(self.frame, width=30)
        self.us_telefono.pack(pady=5)
        
        tk.Label(self.frame, text="Correo electrónico").pack(pady=5)
        self.us_correo_electronico = tk.Entry(self.frame, width=30)
        self.us_correo_electronico.pack(pady=5)
        
        tk.Label(self.frame, text="Dirección").pack(pady=5)
        self.us_direccion = tk.Entry(self.frame, width=30)
        self.us_direccion.pack(pady=5)
        
        tk.Label(self.frame, text="Especialidad").pack(pady=5)
        self.us_especialidad = tk.Entry(self.frame, width=30)
        self.us_especialidad.pack(pady=5)
        
    def limpiar(self):
        limpiar_frame(self.frame)
    
    def ir_lista(self):
        navegar_a_pagina(self.frame, f"Lista {self.tabla}")
        
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
     
        messagebox.showinfo("Actualización", "Se actualizo correctamente")
        navegar_a_pagina(self.frame,"Lista usuarios")
        #messabox, se actualizo correctamente.
        #regresar a lista usuarios
    
    def guardar(self):
        self.crear_usuario()
           
    
          
        
        
        
        
            
            
        
        
        
        
        
        
