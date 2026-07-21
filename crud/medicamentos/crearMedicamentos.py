import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
from tkinter import ttk
from tkcalendar import DateEntry
from herramientas import navegar_a_pagina, limpiar_frame, insertar_registro


class CrearMedicamentos:
    def __init__(self, parent=None, tipo_usuario=None, titulo="Crear"):
        #me queda la duda de que es parent
        self.frame = tk.Frame(parent, bg="#f5f5f5")
        self.frame.pack(fill="both", expand=True)
        self.tabla = 'medicamentos'
        self.tipo_usuario = tipo_usuario 
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
    
        tk.Label(self.frame, text="Nombre comercial").pack(pady=5)
        self.me_nombre_comercial = tk.Entry(self.frame, width=30)
        self.me_nombre_comercial.pack(pady=5)
        
        tk.Label(self.frame, text="Forma farmacéutica").pack(pady=5)
        self.me_forma_farmaceutica = tk.StringVar(value="ninguno")
        self.combo_forma_framaceutica = ttk.Combobox(
            self.frame,
            textvariable=self.me_forma_farmaceutica,
            state="readonly",
            width=27,
            values=["Sólidas", "Semisólidas", "Líquidas","Inhalables"]
        )
        self.combo_forma_framaceutica.pack(pady=5)
        
        tk.Label(self.frame, text="Concentración").pack(pady=5)
        self.me_concentracion = tk.Entry(self.frame, width=30)
        self.me_concentracion.pack(pady=5)
        
        tk.Label(self.frame, text="Fecha de caducidad").pack(pady=5)
        self.me_fecha_caducidad = DateEntry(self.frame, year= 2026)
        self.me_fecha_caducidad.pack(pady=5)
        
        tk.Label(self.frame, text="Descripción").pack(pady=5)
        self.me_descripcion = tk.Text(self.frame, width=40)
        self.me_descripcion.pack(pady=5)
        
    def limpiar(self):
        limpiar_frame(self.frame)
    
    def ir_lista(self):
        navegar_a_pagina(self.frame, f"Lista {self.tabla}", tipo_usuario= self.tipo_usuario)
        
    def guardar_valores(self):
        #actualizar los valores del diccionario con los valores de lo widgets
        self.nuevo_registro ={
                        'me_nombre_comercial': '', 
                        'me_forma_farmaceutica': '', 
                        'me_concentracion': '',
                        'me_fecha_caducidad': "1980-01-01", 
                        'me_descripcion': ''
                        }
        
        self.nuevo_registro["me_nombre_comercial"] = self.me_nombre_comercial.get()
        self.nuevo_registro["me_forma_farmaceutica"] = self.me_forma_farmaceutica.get()
        self.nuevo_registro["me_concentracion"] = self.me_concentracion.get()
        self.nuevo_registro["me_fecha_caducidad"] = self.me_fecha_caducidad.get_date().strftime("%Y-%m-%d")
        self.nuevo_registro["me_descripcion"] = self.me_descripcion.get("1.0","end-1c")
       
    
    def crear_medicamentos(self):
        self.guardar_valores()
        insertar_registro(self.tabla, self.nuevo_registro)
     
        messagebox.showinfo("Crear", "Se creó correctamente el medicamento")
        navegar_a_pagina(self.frame, f"Lista {self.tabla}")
        #messabox, se actualizo correctamente.
        #regresar a lista usuarios
    
    def guardar(self):
        self.crear_medicamentos()
           
        
        
        
        
        
        