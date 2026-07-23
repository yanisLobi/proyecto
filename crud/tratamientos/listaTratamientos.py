import tkinter as tk
import ttkbootstrap as ttkb
from tkinter import ttk
from tkinter import messagebox
from herramientas import navegar_a_pagina, obtener_tabla, borrar_registro


class ListaTratamientos:
    def __init__(self, parent, tipo_usuario=None):
        
        self.tabla = 'tratamientos' 
        self.frame = ttkb.Frame(parent)
        self.frame.pack(fill="both", expand=True)
        self.boton_actualizar = None
        
        if tipo_usuario in ["Doctor", "Administrador"]:
            botones_frame = ttkb.Frame(self.frame)
            botones_frame.pack(pady=(40, 45), padx=20, fill="x")
            botones_frame.grid_columnconfigure(0, weight=1)
            botones_frame.grid_columnconfigure(1, weight=1)
            botones_frame.grid_columnconfigure(2, weight=1)

            ttkb.Button(
                botones_frame,
                text=f"Crear {self.tabla.title()}",
                command=self.ir_crear,
                bootstyle="primary",
            ).grid(row=0, column=0, sticky="ew", padx=6)
            ttkb.Button(
                botones_frame,
                text="Eliminar",
                command=self.borrar,
                bootstyle="danger",
            ).grid(row=0, column=1, sticky="ew", padx=6)
            self.boton_actualizar = ttkb.Button(
                botones_frame,
                text="Actualizar",
                command=self.ir_actualizar,
                state="disabled",
                bootstyle="info",
            )
            self.boton_actualizar.grid(row=0, column=2, sticky="ew", padx=6)
        
            
        self.etiqueta = ttkb.Label(
            self.frame,
            text=f"lista de {self.tabla}",
            font=("Arial", 14, "bold")
        )
        self.etiqueta.pack(pady=(40, 30))
        self.tipo_usuario = tipo_usuario
         
        self.lista_tratamiento = obtener_tabla(self.tabla)

        # Si no hay registros, evitar error con self.lista_tratamiento[0]
        if not self.lista_tratamiento:
            ttkb.Label(
                self.frame,
                text="Sin registros",
                font=("Arial", 12, "italic"),
            ).pack(pady=(20, 0))
            return
        
        usuario = self.lista_tratamiento[0]
        self.columnas = usuario.keys()
        

        self.columnas_tupla = tuple(self.columnas)
        self.tree = ttk. Treeview(self.frame, columns=self.columnas_tupla, show="headings")
        ancho_columna =int(1000/len(self.columnas))
        for columna in self.columnas:
            
            self.tree.heading(columna, text=columna)
            self.tree.column(columna, width=ancho_columna, minwidth=30, stretch=False)

        # Mapear la foreign key con la pagina que se abre cuando le damos doble clic
        self.fk_paginas = {
            "id_paciente": "Actualizar pacientes",
            "id_usuario": "Actualizar usuarios",
        }
        self.tree.bind("<Double-1>", self.on_doble_click)
        self.tree.bind("<Motion>", self.on_mouse_move)
        
        self.recargar_tabla()
        self.tree.bind("<<TreeviewSelect>>", self.on_seleccion)
        self.on_seleccion()
       
        self.tree.pack(pady=(10, 0))

    def recargar_tabla(self):
        #limpiar filas
        for item in self.tree.get_children():
            self.tree.delete(item)
        #llenar tabla
        for usuario in obtener_tabla(self.tabla):
            valores_tupla =tuple(usuario.values())
             
            self.tree.insert("", tk.END, values=valores_tupla)
        self.on_seleccion()
    
    
      
    def ir_crear(self):
    
        navegar_a_pagina(self.frame, f"Crear {self.tabla}", tipo_usuario =self.tipo_usuario)
    def on_seleccion(self, event=None):
        if self.boton_actualizar is None:
            return
        estado = "normal" if self.tree.selection() else "disabled"
        self.boton_actualizar.config(state=estado)
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
        navegar_a_pagina(self.frame, f"Actualizar {self.tabla}", id_seleccionado=id, tipo_usuario=self.tipo_usuario)

    def obtener_celda_evento(self, event):
        region = self.tree.identify_region(event.x, event.y)
        if region != "cell":
            return None

        row_id = self.tree.identify_row(event.y)
        col_id = self.tree.identify_column(event.x)

        if not row_id or not col_id:
            return None

        try:
            col_index = int(col_id.lstrip("#")) - 1
        except ValueError:
            return None

        if col_index < 0 or col_index >= len(self.columnas_tupla):
            return None

        col_name = self.columnas_tupla[col_index]
        values = self.tree.item(row_id, "values")
        if not values:
            return None

        return row_id, col_name, values[col_index]

    def on_doble_click(self, event):
        info = self.obtener_celda_evento(event)
        if not info:
            return

        _, col_name, cell_value = info
        pagina = self.fk_paginas.get(col_name)
        if not pagina:
            return

        if cell_value in (None, ""):
            return

        navegar_a_pagina(
            self.frame,
            pagina,
            id_seleccionado=cell_value,
            tipo_usuario=self.tipo_usuario,
        )

    def on_mouse_move(self, event):
        info = self.obtener_celda_evento(event)
        if info and info[1] in self.fk_paginas:
            self.tree.configure(cursor="hand2")
        else:
            self.tree.configure(cursor="")