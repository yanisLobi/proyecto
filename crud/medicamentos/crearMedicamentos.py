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

        tk.Label(form_frame, text="Nombre comercial", bg="#f5f5f5").grid(row=0, column=0, sticky="w", padx=(0, 10), pady=(0, 16))
        self.me_nombre_comercial = tk.Entry(form_frame, width=30)
        self.me_nombre_comercial.grid(row=0, column=1, sticky="ew", pady=(0, 16))

        tk.Label(form_frame, text="Forma farmacéutica", bg="#f5f5f5").grid(row=0, column=2, sticky="w", padx=(20, 10), pady=(0, 16))
        self.me_forma_farmaceutica = tk.StringVar(value="ninguno")
        self.combo_forma_framaceutica = ttk.Combobox(
            form_frame,
            textvariable=self.me_forma_farmaceutica,
            state="readonly",
            width=27,
            values=["Sólidas", "Semisólidas", "Líquidas","Inhalables"]
        )
        self.combo_forma_framaceutica.grid(row=0, column=3, sticky="ew", pady=(0, 16))

        tk.Label(form_frame, text="Concentración", bg="#f5f5f5").grid(row=1, column=0, sticky="w", padx=(0, 10), pady=(0, 16))
        self.me_concentracion = tk.Entry(form_frame, width=30)
        self.me_concentracion.grid(row=1, column=1, sticky="ew", pady=(0, 16))

        tk.Label(form_frame, text="Fecha de caducidad", bg="#f5f5f5").grid(row=1, column=2, sticky="w", padx=(20, 10), pady=(0, 16))
        self.me_fecha_caducidad = DateEntry(form_frame, year= 2026)
        self.me_fecha_caducidad.grid(row=1, column=3, sticky="w", pady=(0, 16))

        tk.Label(form_frame, text="Descripción", bg="#f5f5f5").grid(row=2, column=0, sticky="nw", padx=(0, 10), pady=(0, 16))
        self.me_descripcion = tk.Text(form_frame, width=40, height=4)
        self.me_descripcion.grid(row=2, column=1, columnspan=3, sticky="ew", pady=(0, 16))
        
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
        navegar_a_pagina(self.frame, f"Lista {self.tabla}", tipo_usuario=self.tipo_usuario)
        #messabox, se actualizo correctamente.
        #regresar a lista usuarios
    
    def guardar(self):
        self.crear_medicamentos()
           
        
        
        
        
        
        