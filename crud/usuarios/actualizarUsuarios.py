from datetime import datetime
from crud.usuarios.crearUsuarios import CrearUsuario
import tkinter as tk
from herramients import navegar_a_pagina, obtener_indice, mostrar_sin_registros
from db_mysql import obtener_registros, actualizar_registro


class ActualizarUsuarios(CrearUsuario):
    def __init__(self, parent, id_seleccionado, usuario={}):

        self.usuario = usuario
        self.tipo_usuario = usuario.get("us_tipo_usuario")

        super().__init__(parent, "Actualizar", usuario=self.usuario)
        self.id_seleccionado = id_seleccionado
        resultado = obtener_registros(
            self.tabla, "id_usuarios", id_seleccionado, False)
        if not resultado:
            mostrar_sin_registros(self.frame, self.tabla)
            return
        self.usuario = resultado[0]

        self.us_tipo_usuario.set(self.tipo_usuario)
        self.us_nombre.insert(0, self.usuario.get("us_nombre", ""))
        self.us_apellidos.insert(0, self.usuario.get("us_apellidos", ""))

        fecha_nacimiento = self.usuario.get("us_fecha_nacimiento")
        if fecha_nacimiento:
            if isinstance(fecha_nacimiento, str):
                fecha_nacimiento = datetime.strptime(
                    fecha_nacimiento, "%Y-%m-%d").date()
            self.us_fecha_nacimiento.set_date(fecha_nacimiento)

        self.us_cedula.insert(0, str(self.usuario.get("us_cedula", "")))
        self.us_telefono.insert(0, str(self.usuario.get("us_telefono", "")))
        self.us_correo_electronico.insert(
            0, self.usuario.get(
                "us_correo_electronico", ""))
        self.us_direccion.insert(0, self.usuario.get("us_direccion", ""))
        self.us_especialidad.set(
            self.usuario.get(
                "us_especialidad",
                "ninguno"))

    def actualizar_usuario(self):
        self.guardar_valores()
        actualizar_registro(
            self.tabla,
            self.nuevo_registro,
            "id_usuarios",
            self.id_seleccionado)

        messagebox.showinfo("Actualización", "Se actualizo correctamente")
        navegar_a_pagina(self.frame, "Lista usuarios", usuario=self.usuario)

    def guardar(self):
        self.actualizar_usuario()
