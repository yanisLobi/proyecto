import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry

from crud.eventos.crearEventos import CrearEventosMongo, COLORES_EVENTO
from herramients import navegar_a_pagina, obtener_indice, mostrar_sin_registros, validar_widget, validar_combo
from db.db_mongo import actualizar_registro, obtener_registros
from db.db_mysql import obtener_valores as _obtener_valores_mysql


class ActualizarEventosMongo(CrearEventosMongo):
    """Muestra un formulario para editar un recordatorio existente.
    Reutiliza el formulario base y lo llena con la información actual."""

    def __init__(self, parent, id_seleccionado, usuario=None):
        """Inicializa la vista de actualización con los datos del recordatorio elegido."""
        super().__init__(parent, "Actualizar", usuario=usuario)
        self.id_seleccionado = str(id_seleccionado)

        eventos = obtener_registros(self.tabla, "id", self.id_seleccionado)
        self.evento = eventos[0] if eventos else None

        if not self.evento:
            mostrar_sin_registros(self.frame, self.tabla)
            return

        # Mismo filtro de rol que al crear; si el tratamiento guardado no está en la
        # lista (inactivo o de otro rol), se carga igualmente para mostrarlo correctamente.
        id_tr_int = int(self.evento.get("id_tr", 0))
        ids_en_lista = {t[0] for t in self.tratamientos}
        if id_tr_int and id_tr_int not in ids_en_lista:
            extra = _obtener_valores_mysql(
                "tratamientos", "id_tratamientos", "tr_nombre", "tr_descripcion",
                solo_activos=False)
            faltante = next((t for t in extra if t[0] == id_tr_int), None)
            if faltante:
                self.tratamientos = list(self.tratamientos) + [faltante]
            self.combo_id_tr.config(values=self.tratamientos)

        self.combo_id_tr.current(obtener_indice(id_tr_int, self.tratamientos))

        # poblar medicamentos del tratamiento guardado y seleccionar el correcto
        id_tr_guardado = str(self.evento.get("id_tr", "")).strip()
        if id_tr_guardado:
            from db.db_mysql import obtener_medicinas_de_tratamientos
            meds = obtener_medicinas_de_tratamientos(id_tr_guardado)
            self.medicamentos = [
                f"{m['id_medicamentos']} {m['me_nombre_comercial']}" for m in meds]
            if self.re_medicamento:
                self.re_medicamento.config(state="readonly", values=self.medicamentos)
                # la DB almacena solo el ID; buscamos la entrada que empiece con ese ID
                med_id_guardado = str(self.evento.get("re_medicamento", "")).strip()
                entrada = next(
                    (v for v in self.medicamentos if v.split()[0] == med_id_guardado),
                    None,
                )
                if entrada:
                    self.re_medicamento.set(entrada)
                elif self.medicamentos:
                    self.re_medicamento.current(0)

        frecuencia = self.evento.get("re_frecuencia", "")
        self.re_frecuencia.delete(0, tk.END)
        self.re_frecuencia.insert(0, str(frecuencia))

        self.re_estado.set(str(self.evento.get("re_estado", "Pendiente")))

        self.re_titulo.delete(0, tk.END)
        self.re_titulo.insert(0, str(self.evento.get("re_titulo", "")))

        self.re_hora_inicio.delete(0, tk.END)
        self.re_hora_inicio.insert(
            0, str(
                self.evento.get(
                    "re_hora_inicio", "")))

        self.re_hora_fin.delete(0, tk.END)
        self.re_hora_fin.insert(0, str(self.evento.get("re_hora_fin", "")))

        self.re_observaciones.delete("1.0", tk.END)
        self.re_observaciones.insert(
            "1.0", str(
                self.evento.get(
                    "re_observaciones", "")))

        color_guardado = str(self.evento.get("re_color", ""))
        nombre_color = next(
            (k for k, v in COLORES_EVENTO.items() if v == color_guardado), list(
                COLORES_EVENTO.keys())[0])
        self.re_color.set(nombre_color)

        fecha = self.evento.get("re_fecha")
        if fecha and isinstance(self.re_fecha, DateEntry):
            try:
                from datetime import date as _date
                if isinstance(fecha, str):
                    partes = fecha.split("-")
                    fecha = _date(int(partes[0]), int(
                        partes[1]), int(partes[2]))
                self.re_fecha.set_date(fecha)
            except Exception:
                pass

    def actualizar_evento(self):
        """Valida los cambios y guarda la información actualizada del recordatorio."""
        if not validar_widget(self.re_titulo, "Título", max_len=100): return
        if not validar_combo(self.id_tr, "Tratamiento"): return
        if not validar_widget(self.re_hora_inicio, "Hora inicio", max_len=5): return
        if not validar_widget(self.re_hora_fin, "Hora fin", max_len=5): return
        self.guardar_valores()
        actualizar_registro(
            self.tabla,
            self.nuevo_registro,
            "id",
            self.id_seleccionado)
        messagebox.showinfo("Actualización",
                            "Se actualizó correctamente el recordatorio")
        navegar_a_pagina(self.frame, "Lista eventos", usuario=self.usuario)

    def guardar(self):
        """Ejecuta la actualización del recordatorio desde el botón guardar."""
        self.actualizar_evento()
