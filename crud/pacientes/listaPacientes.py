import tkinter as tk
from tkinter import ttk

from herramientas import navegar_a_pagina

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
        self.usuarios = [{"nombre": "yanet", "apellido": "lazaro", "edad":"20"}, {"nombre": "juana", "apellido": "lazaro", "edad":"23"},
                    {"nombre": "karla", "apellido": "lcamscdv", "edad":"55"}]
  
        tipo_usuario = ""
        if tipo_usuario == "Doctor" or tipo_usuario == "Administrador":
            tk.Button(self.frame, text="Mostrar información",command= self.mostrar_crear_usuario)
    
        tree = ttk. Treeview(self.frame, columns=("nombre","apellido", "edad"), show="headings")
        tree.heading("nombre", text="Nombre")
        tree.heading("apellido", text="Apellido")
        tree.heading("edad", text="Edad")
        for usuario in self.usuarios:
            
            tree.insert("", tk.END, values=(usuario.get("nombre"),usuario.get("apellido"),usuario.get("edad")))
        tree.pack(pady=10)

        
    def ir_crear(self):
    
        navegar_a_pagina(self.frame, "Crear pacientes")

        