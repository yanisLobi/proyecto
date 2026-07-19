from datetime import datetime
from crud.medicamentos.crearMedicamentos import CrearMedicamentos
from tkinter import messagebox
import tkinter as tk
from herramientas import obtener_registro, navegar_a_pagina, actualizar_registro


class ActualizarMedicamentos(CrearMedicamentos):
    def __init__(self, parent, id_seleccionado):
        super().__init__(parent, "Actualizar")
        self.id_seleccionado=id_seleccionado
        self.medicamento = obtener_registro(self.tabla, "id_me", id_seleccionado)
        if not self.medicamento:
            messagebox.showinfo("Sin datos", "No se encontró el usuario seleccionado")
            return

        self.me_nombre_comercial.insert(0, self.medicamento.get("me_nombre_comercial", ""))
        self.me_forma_farmaceutica.set(self.medicamento.get("me_forma_farmaceutica", "ninguno"))
        self.me_concentracion.insert(0, self.medicamento.get("me_concentracion", ""))

        fecha_caducidad = self.medicamento.get("me_fecha_caducidad")
        if fecha_caducidad:
            if isinstance(fecha_caducidad, str):
                fecha_caducidad = datetime.strptime(fecha_caducidad, "%Y-%m-%d").date()
            self.me_fecha_caducidad.set_date(fecha_caducidad)

        self.me_descripcion.insert(tk.END, str(self.medicamento.get("me_descripcion", "")))
    
    def actualizar_medicamento(self):
        self.guardar_valores()
        actualizar_registro(self.tabla, self.nuevo_registro, "id_me", self.id_seleccionado)
     
        messagebox.showinfo("Actualización", "Se actualizo correctamente")
        navegar_a_pagina(self.frame,"Lista medicamentos")
        
    def guardar(self):
        self.actualizar_medicamento()
    
   # def actualizar_usuario(self):
        #dicc
        #construir sql 
        #conexion, cursor, ejecutar un update
        #messabox, se actualizo correctamente.
        #regresar a lista usuarios
        
       
       
       
       
       
      
    
    