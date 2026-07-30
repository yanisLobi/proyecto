import ttkbootstrap as ttkb


from db_mongo import obtener_registros
from herramients import navegar_a_pagina


class ConsultarEventosMongo:
	def __init__(self, parent, id_seleccionado, usuario=None):
		self.frame = ttkb.Frame(parent)
		self.frame.pack(fill="both", expand=True)
		self.tabla = "consultas"
		self.usuario = usuario or {}

		ttkb.Label(
			self.frame,
			text="Consultar recordatorios",
			font=("Arial", 14, "bold")
		).pack(pady=(40, 20))

		evento = obtener_registros(self.tabla, "id", str(id_seleccionado))
		self.evento = evento[0] if evento else {}

		form_frame = ttkb.Frame(self.frame)
		form_frame.pack(padx=20, pady=(20, 30), fill="x")
		form_frame.grid_columnconfigure(0, weight=0)
		form_frame.grid_columnconfigure(1, weight=1)

		campos = [
			"id",
			"id_tr",
			"re_estado",
			"re_observaciones",
			"re_titulo",
			"re_hora_fin",
			"re_hora_inicio",
			"re_fecha",
		]

		for indice, campo in enumerate(campos):
			ttkb.Label(form_frame, text=campo).grid(row=indice, column=0, sticky="w", padx=(0, 10), pady=(0, 12))
			ttkb.Label(form_frame, text=str(self.evento.get(campo, ""))).grid(row=indice, column=1, sticky="w", pady=(0, 12))

		ttkb.Button(
			self.frame,
			text="Volver",
			command=self.ir_lista,
			bootstyle="secondary",
		).pack(pady=(10, 20))

	def ir_lista(self):
		navegar_a_pagina(self.frame, "Lista eventos", usuario=self.usuario)
