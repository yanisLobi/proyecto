import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry

from crud.eventos.crearEventos import CrearEventosMongo, COLORES_EVENTO
from herramients import navegar_a_pagina, obtener_indice
from db_mongo import actualizar_registro, obtener_registros


class ActualizarEventosMongo(CrearEventosMongo):
    def __init__(self, parent, id_seleccionado, usuario=None):
        super().__init__(parent, "Actualizar", usuario=usuario)
        self.id_seleccionado = str(id_seleccionado)

        eventos = obtener_registros(self.tabla, "id", self.id_seleccionado)
        self.evento = eventos[0] if eventos else None

        if not self.evento:
            messagebox.showinfo("Sin datos",
                                "No se encontró el recordatorio seleccionado")
            navegar_a_pagina(self.frame, "Lista eventos", usuario=self.usuario)
            return

        self.combo_id_tr.current(obtener_indice(
            str(self.evento.get("id_tr", "")), self.tratamientos))

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
        self.actualizar_evento()
