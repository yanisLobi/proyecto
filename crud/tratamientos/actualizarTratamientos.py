from datetime import datetime
from crud.tratamientos.crearTratamientos import CrearTratamientos
from tkinter import messagebox
import tkinter as tk
from herramientas import obtener_registro, navegar_a_pagina, actualizar_registro


class ActualizarTratamientos(CrearTratamientos):
    def __init__(self, parent, id_seleccionado):
        super().__init__(parent, "Actualizar")
        self.id_seleccionado=id_seleccionado
        self.tratamientos = obtener_registro(self.tabla, "id_tratamiento", id_seleccionado)
        if not self.tratamientos:
            messagebox.showinfo("Sin datos", "No se encontró el usuario seleccionado")
            return

        self.tr_nombre.insert(0, self.tratamientos.get("tr_nombre", ""))
        fecha_caducidad = self.tratamientos.get("me_fecha_caducidad")
        
        #crear las dos fechas
        if fecha_caducidad:
            if isinstance(fecha_caducidad, str):
                fecha_caducidad = datetime.strptime(fecha_caducidad, "%Y-%m-%d").date()
            self.me_fecha_caducidad.set_date(fecha_caducidad)

        self.tr_descripcion.insert(tk.END, str(self.tratamientos.get("tr_descripcion", "")))
    
    def actualizar_tratamientos(self):
        self.guardar_valores()
        actualizar_registro(self.tabla, self.nuevo_registro, "id_tratamiento", self.id_seleccionado)
     
        messagebox.showinfo("Actualización", "Se actualizo correctamente")
        navegar_a_pagina(self.frame,"Lista tratamientoss")
        
    def guardar(self):
        self.actualizar_tratamientos()
    