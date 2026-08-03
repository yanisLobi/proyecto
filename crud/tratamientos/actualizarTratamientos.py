from datetime import datetime
from crud.tratamientos.crearTratamientos import CrearTratamientos
from tkinter import messagebox, ttk
import tkinter as tk
from typing import Any, cast
from herramients import navegar_a_pagina, obtener_indice, regresar_string
from db_mysql import insertar_receta, obtener_registros, actualizar_registro, obtener_medicinas_de_tratamientos, eliminar_recetas_tratamiento, obtener_valores_recetas


class ActualizarTratamientos(CrearTratamientos):
    def __init__(self, parent, id_seleccionado, usuario={}):

        self.usuario = usuario
        self.tipo_usuario = usuario.get("us_tipo_usuario")

        super().__init__(parent, "Actualizar", usuario=self.usuario)

        self.id_seleccionado = id_seleccionado
        self.tratamientos = cast(dict[str, Any], obtener_registros(
            self.tabla, "id_tratamientos", id_seleccionado) or {})[0]
        if not self.tratamientos:
            messagebox.showinfo("Sin datos",
                                "No se encontró el usuario seleccionado")
            return

        self.tr_nombre.insert(0, self.tratamientos.get("tr_nombre", ""))

        fecha_inicio = self.tratamientos.get("tr_fecha_inicio")
        if fecha_inicio:
            if isinstance(fecha_inicio, str):
                fecha_inicio = datetime.strptime(
                    fecha_inicio, "%Y-%m-%d").date()
            self.tr_fecha_inicio.set_date(fecha_inicio)

        fecha_final = self.tratamientos.get("tr_fecha_final")
        if fecha_final:
            if isinstance(fecha_final, str):
                fecha_final = datetime.strptime(fecha_final, "%Y-%m-%d").date()
            self.tr_fecha_final.set_date(fecha_final)

        self.tr_descripcion.insert(
            tk.END, str(
                self.tratamientos.get(
                    "tr_descripcion", "")))

        self.id_paciente_seleccionado = self.tratamientos.get("id_paciente")
        self.combo_id_paciente.current(
            obtener_indice(
                self.id_paciente_seleccionado,
                self.valores_pacientes))

        self.id_doctor_seleccionado = self.tratamientos.get("id_doctor")
        self.combo_id_doctor.current(
            obtener_indice(
                self.id_doctor_seleccionado,
                self.valores_doctor))

        medicamentos = obtener_medicinas_de_tratamientos(self.id_seleccionado)
        self.lista_recetas = obtener_valores_recetas(self.id_seleccionado)

        columnas = tuple(self.lista_recetas[0].keys())

        self.tree = ttk.Treeview(
            self.frame,
            columns=columnas,
            show="headings"
        )

        for columna in columnas:
            self.tree.heading(columna, text=regresar_string(columna))

        for receta in self.lista_recetas:
            self.tree.insert("", tk.END, values=tuple(receta.values()))

        self.tree.pack()

        ids_medicamentos = {
            medicamento["id_medicamentos"]
            for medicamento in medicamentos
        }

        for id_medicamento in ids_medicamentos:
            if id_medicamento in self.check_medicamentos:
                self.check_medicamentos[id_medicamento].set(True)

    def actualizar_tratamientos(self):
        self.guardar_valores()
        actualizar_registro(
            self.tabla,
            self.nuevo_registro,
            "id_tratamientos",
            self.id_seleccionado)

        eliminar_recetas_tratamiento(self.id_seleccionado)

        for id_medicamento in self.medicamentos_seleccionados:
            insertar_receta(self.id_seleccionado, id_medicamento)

        messagebox.showinfo("Actualización", "Se actualizo correctamente")
        navegar_a_pagina(
            self.frame,
            "Lista tratamientos",
            usuario=self.usuario)

    def guardar(self):
        self.actualizar_tratamientos()
