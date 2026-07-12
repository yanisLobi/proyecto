import tkinter as tk
from listaPacientes import ListaPacientes
from tkinter import messagebox

class ActualizarPacientes:
    def __init__(self, parent):
        self.frame = tk.Frame(parent, bg="#f5f5f5")
        self.frame.pack(fill="both", expand=True)

        self.etiqueta = tk.Label(
            self.frame,
            text="ActualizarPacientes",
            font=("Arial", 14, "bold"),
            bg="#f5f5f5",
            fg="#2c3e50"
        )
        self.etiqueta.pack(pady=20)
    
    def actualizar(self):
        if self.usuarios is None:
            messagebox.showwarning("Advertencia", "selecciono un pacientes")
            return
        
        #falta importar crear pacientes
        if not self.validar_campos():
            #si la validacion fallo, termina el metodo
            return
        
        