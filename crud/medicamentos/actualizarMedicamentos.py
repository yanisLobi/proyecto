from datetime import datetime
from tkinter import messagebox
from crud.medicamentos.crearMedicamentos import CrearMedicamentos
import tkinter as tk
from herramients import navegar_a_pagina, obtener_indice, mostrar_sin_registros, validar_widget, validar_combo
from db_mysql import obtener_registros, actualizar_registro


class ActualizarMedicamentos(CrearMedicamentos):
    def __init__(self, parent, id_seleccionado, usuario={}):
        super().__init__(parent, titulo="Actualizar")
        self.usuario = usuario
        self.tipo_usuario = usuario.get("us_tipo_usuario")
        self.id_seleccionado = id_seleccionado
        resultado = obtener_registros(
            self.tabla, "id_medicamentos", id_seleccionado, False)
        if not resultado:
            mostrar_sin_registros(self.frame, self.tabla)
            return
        self.medicamento = resultado[0]

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
        if not validar_widget(self.me_nombre_comercial, "Nombre comercial", max_len=50): return
        if not validar_widget(self.me_concentracion, "Concentración", max_len=50): return
        if not validar_widget(self.me_descripcion, "Descripción", max_len=100, requerido=False): return
        if not validar_combo(self.me_forma_farmaceutica, "Forma farmacéutica"): return
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
