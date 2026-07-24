from datetime import datetime
from crud.pacientes.crearPacientes import CrearPacientes
from tkinter import messagebox, ttk
import tkinter as tk
from herramientas import obtener_registro, navegar_a_pagina, actualizar_registro, obtener_tabla, obtener_tabla_condicion, regresar_string


class ActualizarPacientes(CrearPacientes):
    def __init__(self, parent, id_seleccionado, tipo_usuario=None):
        super().__init__(parent, "Actualizar", tipo_usuario=tipo_usuario)
        self.id_seleccionado=id_seleccionado
        
        self.pacientes = obtener_registro(self.tabla, "id_pacientes", id_seleccionado)
        if not self.pacientes:
            messagebox.showinfo("Sin datos", "No se encontró el usuario seleccionado")
            return

        self.pa_nombre.insert(0, self.pacientes.get("pa_nombre", ""))
        self.pa_apellidos.insert(0, self.pacientes.get("pa_apellidos", ""))

        fecha_nacimiento = self.pacientes.get("me_fecha_caducidad")
        if fecha_nacimiento:
            if isinstance(fecha_nacimiento, str):
                fecha_nacimiento = datetime.strptime(fecha_nacimiento, "%Y-%m-%d").date()
            self.pa_fecha_nacimiento.set_date(fecha_nacimiento)

        self.pa_nombre_contacto_emergencia.insert(0, self.pacientes.get("pa_nombre_contacto_emergencia", ""))
        self.id_enfermera_seleccionado = self.pacientes.get("id_enfermera_principal")
        self.pa_tel_contacto_emergencia.insert(0, str(self.pacientes.get("pa_tel_contacto_emergencia", "")))
        self.combo_id_enfermera.current(1)
       
        
        
        
        #
        
        self.lista_tratamientos = obtener_tabla_condicion("tratamientos", "id_paciente", id_seleccionado)
        
        tratamiento = self.lista_tratamientos[0]
        self.columnas = tratamiento.keys()
        print(self.lista_tratamientos)

        self.columnas_tupla = tuple(self.columnas)
        self.tree = ttk. Treeview(self.frame, columns=self.columnas_tupla, show="headings")
        ancho_columna =int(1000/len(self.columnas))
        for columna in self.columnas:
            
            self.tree.heading(columna, text=regresar_string(columna))
            self.tree.column(columna, width=ancho_columna, minwidth=30, stretch=False)
    
        self.tree.pack(pady=(10, 0))
        
        for tratamiento in self.lista_tratamientos:
            valores_tupla =tuple(tratamiento.values())
                                 
            self.tree.insert("", tk.END, values=valores_tupla)
                            
                    
     
        
        
        
    
    def actualizar_pacientes(self):
        self.guardar_valores()
        actualizar_registro(self.tabla, self.nuevo_registro, "id_pacientes", self.id_seleccionado)
     
        messagebox.showinfo("Actualización", "Se actualizo correctamente")
        navegar_a_pagina(self.frame, "Lista pacientes", tipo_usuario=self.tipo_usuario)
        
    def guardar(self):
        self.actualizar_pacientes()
    
    
    
        