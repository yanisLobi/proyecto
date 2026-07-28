import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry

from crud.eventos.crearEventos import CrearEventosMongo
from herramients import navegar_a_pagina_mongo as navegar_a_pagina
from db_mongo import actualizar_registro, obtener_registros


class ActualizarEventosMongo(CrearEventosMongo):
	def __init__(self, parent, id_seleccionado, usuario=None):
		super().__init__(parent, "Actualizar", usuario=usuario)
		self.id_seleccionado = str(id_seleccionado)

		eventos = obtener_registros(self.tabla, "id", self.id_seleccionado)
		self.evento = eventos[0] if eventos else None

		if not self.evento:
			messagebox.showinfo("Sin datos", "No se encontró el evento seleccionado")
			navegar_a_pagina(self.frame, "Lista eventos", usuario=self.usuario)
			return


		self.id_tr.delete(0, tk.END)
		self.id_tr.insert(0, str(self.evento.get("id_tr", "")))

		self.re_estado.set(str(self.evento.get("re_estado", "Pendiente")))

		self.re_titulo.delete(0, tk.END)
		self.re_titulo.insert(0, str(self.evento.get("re_titulo", "")))

		self.re_hora_inicio.delete(0, tk.END)
		self.re_hora_inicio.insert(0, str(self.evento.get("re_hora_inicio", "")))

		self.re_hora_fin.delete(0, tk.END)
		self.re_hora_fin.insert(0, str(self.evento.get("re_hora_fin", "")))

		self.re_observaciones.delete("1.0", tk.END)
		self.re_observaciones.insert("1.0", str(self.evento.get("re_observaciones", "")))

		fecha = self.evento.get("re_fecha")
		if fecha and isinstance(self.re_fecha, DateEntry):
			try:
				self.re_fecha.set_date(str(fecha))
			except Exception:
				pass

	def actualizar_evento(self):
		self.guardar_valores()
		actualizar_registro(self.tabla, self.nuevo_registro, "id", self.id_seleccionado)
		messagebox.showinfo("Actualización", "Se actualizó correctamente el evento")
		navegar_a_pagina(self.frame, "Lista eventos", usuario=self.usuario)

	def guardar(self):
		self.actualizar_evento()
