import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from herramientas import navegar_a_pagina, obtener_tabla, borrar_registro


class ListaPacientes:
    def __init__(self, parent, tipo_usuario=None):
        
        self.tabla = 'pacientes' 
        self.frame = tk.Frame(parent, bg="#f5f5f5")
        self.frame.pack(fill="both", expand=True)
        
        if tipo_usuario in ["Doctor", "Administrador"]:
            tk.Button(self.frame, text=f"Crear {self.tabla.title()}", command=self.ir_crear).pack(pady=10)
            tk.Button(self.frame, text="Eliminar", command=self.borrar).pack(pady=10)
            tk.Button(self.frame, text="Actualizar", command=self.ir_actualizar).pack(pady=10)
        
            
        self.etiqueta = tk.Label(
            self.frame,
            text=f"lista de {self.tabla}",
            font=("Arial", 14, "bold"),
            bg="#f5f5f5",
            fg="#2c3e50"
        )
        self.etiqueta.pack(pady=20)
        
         
        self.lista_pacientes = obtener_tabla(self.tabla)
        
        usuario = self.lista_pacientes[0]
        self.columnas = usuario.keys()
        

        self.columnas_tupla = tuple(self.columnas)
        self.tree = ttk. Treeview(self.frame, columns=self.columnas_tupla, show="headings")
        ancho_columna =int(1000/len(self.columnas))
        for columna in self.columnas:
            
            self.tree.heading(columna, text=columna)
            self.tree.column(columna, width=ancho_columna, minwidth=30, stretch=False)
        
        self.recargar_tabla()
       
        self.tree.pack(pady=0)

    def recargar_tabla(self):
        #limpiar filas
        for item in self.tree.get_children():
            self.tree.delete(item)
        #llenar tabla
        for usuario in obtener_tabla(self.tabla):
            valores_tupla =tuple(usuario.values())
             
            self.tree.insert("", tk.END, values=valores_tupla)
    
    
      
    def ir_crear(self):
    
        navegar_a_pagina(self.frame, f"Crear {self.tabla}")
    def obtener_id_seleccionado(self):
        item_id = self.tree.selection()
        if not item_id:
            messagebox.showinfo("Error", f"Debes seleccionar un {self.tabla.title()} de la tabla")
            return

        self.valores = self.tree.item(item_id[0], "values")
        if not self.valores:
            messagebox.showinfo("Error", "La fila seleccionada no tiene datos")
            return

        return self.valores[0]       
    def borrar(self):
        
        id = self.obtener_id_seleccionado()
        borrar_registro(self.tabla, self.columnas_tupla[0], id)
        messagebox.showinfo("Eliminar", f"Haz eliminado el {self.tabla.title()} con ID = {id}")
        self.recargar_tabla()
    
    def ir_actualizar(self):
        
        item_id = self.tree.selection()
        if not item_id:
            messagebox.showinfo("Sin selección", f"seleccione un {self.tabla} ")
            
            return
        
        id = self.obtener_id_seleccionado()
        navegar_a_pagina(self.frame, f"Actualizar {self.tabla}", id)
        #ActualizarUsuario(self.frame, self.id_selccionado)
        
        