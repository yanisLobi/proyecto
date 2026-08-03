from datetime import datetime
from crud.medicamentos.crearMedicamentos import CrearMedicamentos
from tkinter import messagebox
import tkinter as tk
from herramients import navegar_a_pagina, obtener_indice
from db_mysql import obtener_registros, actualizar_registro


class ActualizarMedicamentos(CrearMedicamentos):
    def __init__(self, parent, id_seleccionado, usuario={}):
        super().__init__(parent, titulo="Actualizar")
        self.usuario = usuario
        self.tipo_usuario = usuario.get("us_tipo_usuario")
        self.id_seleccionado = id_seleccionado
        self.medicamento = obtener_registros(
            self.tabla, "id_medicamentos", id_seleccionado)[0]
        if not self.medicamento:
            messagebox.showinfo("Sin datos",
                                "No se encontró el usuario seleccionado")
            return

        self.me_nombre_comercial.insert(
            0, self.medicamento.get(
                "me_nombre_comercial", ""))
        self.me_forma_farmaceutica.set(
            self.medicamento.get(
                "me_forma_farmaceutica",
                "ninguno"))
        self.me_concentracion.insert(
            0, self.medicamento.get(
                "me_concentracion", ""))

        fecha_caducidad = self.medicamento.get("me_fecha_caducidad")
        if fecha_caducidad:
            if isinstance(fecha_caducidad, str):
                fecha_caducidad = datetime.strptime(
                    fecha_caducidad, "%Y-%m-%d").date()
            self.me_fecha_caducidad.set_date(fecha_caducidad)

        self.me_descripcion.insert(
            tk.END, str(
                self.medicamento.get(
                    "me_descripcion", "")))

    def actualizar_medicamento(self):
        self.guardar_valores()
        actualizar_registro(
            self.tabla,
            self.nuevo_registro,
            "id_medicamentos",
            self.id_seleccionado)

        messagebox.showinfo("Actualización", "Se actualizo correctamente")
        navegar_a_pagina(
            self.frame,
            "Lista medicamentos",
            usuario=self.usuario)

    def guardar(self):
        self.actualizar_medicamento()

   # def actualizar_usuario(self):
        # dicc
        # construir sql
        # conexion, cursor, ejecutar un update
        # messabox, se actualizo correctamente.
        # regresar a lista usuarios
