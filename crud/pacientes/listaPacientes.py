import tkinter as tk
from tkinter import ttk
from conexion import conectar


from herramientas import navegar_a_pagina, obtener_tabla


class ListaPacientes:
    def __init__(self, parent):
        self.frame = tk.Frame(parent, bg="#f5f5f5")
        self.frame.pack(fill="both", expand=True)
        tk.Button(self.frame, text="Crear Paciente", command=self.ir_crear).pack(pady=10)

        self.etiqueta = tk.Label(
            self.frame,
            text="Lista de pacientes",
            font=("Arial", 14, "bold"),
            bg="#f5f5f5",
            fg="#2c3e50"
        )
        self.etiqueta.pack(pady=20)
        
        lista_pacientes = obtener_tabla('pacientes')
        
        paciente = lista_pacientes[0]
        columnas = paciente.keys()
        
        tipo_usuario = ""
        if tipo_usuario == "Doctor" or tipo_usuario == "Administrador":
            tk.Button(self.frame, text="Mostrar información",command= self.mostrar_crear_usuario)

        columnas_tupla = tuple(columnas)
        tree = ttk. Treeview(self.frame, columns=columnas_tupla, show="headings")
        for columna in columnas:
            
            tree.heading(columna, text=columna)
        
        
        for paciente in lista_pacientes:
            valores_tupla =tuple(paciente.values())
             
            
            tree.insert("", tk.END, values=valores_tupla)
        tree.pack(pady=10)

        
    def ir_crear(self):
    
        navegar_a_pagina(self.frame, "Crear pacientes")

        