import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
from tkinter import ttk
from tkcalendar import DateEntry
from herramientas import navegar_a_pagina, limpiar_frame, insertar_registro


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
        
        tk.Button(self.frame, text="Limpiar campos", command=self.limpiar).pack(pady=10)
        tk.Button(self.frame, text="Cancelar", command=self.ir_lista).pack(pady=10)
        tk.Button(self.frame, text="Guardar", command=self.guardar).pack(pady=10)
    
        tk.Label(self.frame, text="Nombre comercial").pack(pady=5)
        self.me_nombre_comercial = tk.Entry(self.frame, width=30)
        self.me_nombre_comercial.pack(pady=5)
        
        
        tk.Label(self.frame, text="Forma farmecéutica").pack(pady=5)
        self.me_tipo = tk.StringVar(value="ninguno")
        tk.Radiobutton(self.frame, text="Sólidas", variable=self.me_tipo, value="Sólidas").pack()
        tk.Radiobutton(self.frame, text="Semisólidas", variable=self.me_tipo, value="Semisólidas").pack()
        tk.Radiobutton(self.frame, text="Líquidas", variable=self.me_tipo, value="Líquidas").pack()
        tk.Radiobutton(self.frame, text="Inhalables", variable=self.me_tipo, value="Inhalables").pack()
        
        tk.Label(self.frame, text="Concentración").pack(pady=5)
        self.me_concentracion = tk.Entry(self.frame, width=30)
        self.me_concentracion.pack(pady=5)
        
        tk.Label(self.frame, text="Fecha de caducidad").pack(pady=5)
        self.me_fecha_caducidad = DateEntry(self.frame, year= 2026)
        self.me_fecha_caducidad.pack(pady=5)
        
        tk.Label(self.frame, text="Descripción")
        me_descripcion = tk.Text(self.frame, height=4, width=40)
        me_descripcion.pack(pady=5)
        
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
        
    
    def crear_registro(self):
        self.guardar_valores()
        insertar_registro(self.tabla, self.nuevo_registro)
     
        messagebox.showinfo("Actualización", "Se actualizo correctamente")
        navegar_a_pagina(self.frame,f"Lista {self.tabla}")
        #messabox, se actualizo correctamente.
        #regresar a lista usuarios
    
    def guardar(self):
        self.crear_usuario()
           
        
        
        
        
        
        