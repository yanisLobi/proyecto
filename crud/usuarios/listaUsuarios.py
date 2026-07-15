import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from herramientas import navegar_a_pagina, obtener_tabla, borrar_registro

class ListaUsuarios:
    def __init__(self, parent):
        
        self.tabla = 'usuarios' 
        self.frame = tk.Frame(parent, bg="#f5f5f5")
        self.frame.pack(fill="both", expand=True)
        tk.Button(self.frame, text=f"Crear {self.tabla.title()}", command=self.ir_crear).pack(pady=10)
        tk.Button(self.frame, text="Eliminar", command=self.borrar).pack(pady=10)
        tk.Button(self.frame, text="Actualizar", command=self.actualizar).pack(pady=10)

        self.etiqueta = tk.Label(
            self.frame,
            text=f"lista de {self.tabla}",
            font=("Arial", 14, "bold"),
            bg="#f5f5f5",
            fg="#2c3e50"
        )
        self.etiqueta.pack(pady=20)
        
         
        lista_usuarios = obtener_tabla(self.tabla)
        
        usuario = lista_usuarios[0]
        self.columnas = usuario.keys()
        
        tipo_usuario = ""
        if tipo_usuario == "Doctor" or tipo_usuario == "Administrador":
            tk.Button(self.frame, text="Mostrar información",command= self.mostrar_crear_usuario)

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
        
    def borrar(self):
        
        item_id = self.tree.selection()
        if not item_id:
            messagebox.showinfo("Error", f"Debes seleccionar un {self.tabla.title()} de la tabla")
            return

        valores = self.tree.item(item_id[0], "values")
        if not valores:
            messagebox.showinfo("Error", "La fila seleccionada no tiene datos")
            return

        id_valor = valores[0]
        borrar_registro(self.tabla, self.columnas_tupla[0], id_valor)
        messagebox.showinfo("Eliminar", f"Haz eliminado el {self.tabla.title()} con ID = {id_valor}")
        self.recargar_tabla()
    
    def actualizar(self):
        
        item_id = self.tree.selection()
        if not item_id:
            messagebox.showinfo("Sin selección", f"seleccione un {self.tabla} ")
            
            return
    def mostrar_registros(self):
        self.ir_crear()
        
        
        
    #obtenemos los nuevos campos que agrgaron
    
            
        
        