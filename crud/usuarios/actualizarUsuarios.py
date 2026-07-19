from datetime import datetime
from crud.usuarios.crearUsuarios import CrearUsuario
import tkinter as tk
from tkinter import messagebox
from herramientas import obtener_registro, navegar_a_pagina, actualizar_registro


class ActualizarUsuarios(CrearUsuario):
    def __init__(self, parent, id_seleccionado):
        super().__init__(parent, "Actualizar")
        self.id_seleccionado=id_seleccionado
        self.usuario = obtener_registro(self.tabla, "id_usuarios", id_seleccionado)
        if not self.usuario:
            messagebox.showinfo("Sin datos", "No se encontró el usuario seleccionado")
            return

        self.us_tipo_usuario.set(self.usuario.get("us_tipo_usuario", "ninguno"))
        self.us_nombre.insert(0, self.usuario.get("us_nombre", ""))
        self.us_apellidos.insert(0, self.usuario.get("us_apellidos", ""))

        fecha_nacimiento = self.usuario.get("us_fecha_nacimiento")
        if fecha_nacimiento:
            if isinstance(fecha_nacimiento, str):
                fecha_nacimiento = datetime.strptime(fecha_nacimiento, "%Y-%m-%d").date()
            self.us_fecha_nacimiento.set_date(fecha_nacimiento)

        self.us_contra.insert(0, self.usuario.get("us_contraseña", ""))
        self.us_telefono.insert(0, str(self.usuario.get("us_telefono", "")))
        self.us_correo_electronico.insert(0, self.usuario.get("us_correo_electronico", ""))
        self.us_direccion.insert(0, self.usuario.get("us_direccion", ""))
        self.us_especialidad.insert(0, self.usuario.get("us_especialidad", ""))
    
    def actualizar_usuario(self):
        self.guardar_valores()
        actualizar_registro(self.tabla, self.nuevo_registro, "id_usuarios", self.id_seleccionado)
     
        messagebox.showinfo("Actualización", "Se actualizo correctamente")
        navegar_a_pagina(self.frame,"Lista usuarios")
        
    def guardar(self):
        self.actualizar_usuario()
    
   # def actualizar_usuario(self):
        #dicc
        #construir sql 
        #conexion, cursor, ejecutar un update
        #messabox, se actualizo correctamente.
        #regresar a lista usuarios
        
       
       
       
       
       
      
    