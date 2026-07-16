import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from herramientas import navegar_a_pagina, obtener_tabla, borrar_registro
from conexion import conectar

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
        
         
        self.lista_usuarios = obtener_tabla(self.tabla)
        
        usuario = self.lista_usuarios[0]
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

        self.valores = self.tree.item(item_id[0], "values")
        if not self.valores:
            messagebox.showinfo("Error", "La fila seleccionada no tiene datos")
            return

        id_valor = self.valores[0]
        borrar_registro(self.tabla, self.columnas_tupla[0], id_valor)
        messagebox.showinfo("Eliminar", f"Haz eliminado el {self.tabla.title()} con ID = {id_valor}")
        self.recargar_tabla()
    
    def actualizar(self):
        
        item_id = self.tree.selection()
        if not item_id:
            messagebox.showinfo("Sin selección", f"seleccione un {self.tabla} ")
            
            return
        self.ir_crear()
        self.ir_crear
        conexion = conectar()
        cursor = conexion.cursor(dictionary=True)
        self.valores = self.tree(item_id[0], "values")
        id_valor = self.valores[0]
        query = f"SELECT * FROM {self.tabla} WHERE `{self.columnas_tupla[0]}` = %s"
        cursor.execute(query, (id_valor,))
        usuario = cursor.fetchone()
        return usuario
        
        self.us_tipo_usuario.set(0)
        self.us_tipo_usuario.insert(0, usuario["us_tipo_usuario"])
        
        self.us_nombre.delete(0, tk.END)
        self.us_nombre.insert(0, usuario["us_nombre"])
        
        self.us_apellidos.delete(0, tk.END)
        self.us_apellidos.insert(0, usuarios["us_apellidos"])
        
        self.us_fecha_nacimiento.delete(0, 'end')
        self.us_fecha_nacimiento.insert(0, usuario["us_fecha_nacimiento"])
        
        self.us_telefono.delete(0, tk.END)
        self.us_telefono.insert(0, usuario["us_telefono"])
        
        self.us_correo_electronico.delete(0, tk.END)
        self.us_correo_electronico.insert(0, usuario["us_correo_electronico"])
        
        self.us_direccion.delete(0, tk.END)
        self.us_direccion.insert(0, usuario["us_direccion"])
        
        self.us_especialidad.set(0)
        self.us_especialidad.insert(0, usuario["us_especialidad"])
        
        

    
        

        
    #obtenemos los nuevos campos que agrgaron
    
            
        
        