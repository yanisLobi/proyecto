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
        
        fecha_inicio = self.tratamientos.get("tr_fecha_inicio")
        if fecha_inicio:
            if isinstance(fecha_inicio, str):
                fecha_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d").date()
            self.tr_fecha_inicio.set_date(fecha_inicio)

        fecha_final = self.tratamientos.get("tr_fecha_final")
        if fecha_inicio:
            if isinstance(fecha_final, str):
                fecha_final = datetime.strptime(fecha_final, "%Y-%m-%d").date()
            self.tr_fecha_final.set_date(fecha_final)

        self.tr_descripcion.insert(tk.END, str(self.tratamientos.get("tr_descripcion", "")))
    
    def actualizar_tratamientos(self):
        self.guardar_valores()
        actualizar_registro(self.tabla, self.nuevo_registro, "id_tratamiento", self.id_seleccionado)
     
        messagebox.showinfo("Actualización", "Se actualizo correctamente")
        navegar_a_pagina(self.frame,"Lista tratamientoss")
        
    def guardar(self):
        self.actualizar_tratamientos()
    