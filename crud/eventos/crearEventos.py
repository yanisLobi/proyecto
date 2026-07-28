import tkinter as tk
import ttkbootstrap as ttkb
from tkinter import messagebox
from tkcalendar import DateEntry
from tkinter import ttk

from herramients import limpiar_frame, navegar_a_pagina_mongo as navegar_a_pagina
from db_mongo import insertar_registro

class CrearEventos:
    def __init__(self, parent):
        self.frame = ttkb.Frame(parent)
        self.frame.pack(fill="both", expand=True)
    
        self.etiqueta = ttkb.Label(
            self.frame,
            text="Crear pacientes",
            font=("Arial", 14, "bold")
        )
        self.etiqueta.pack(pady=(40, 30))

        form_frame = ttkb.Frame(self.frame)
        form_frame.pack(padx=20, pady=(20, 30), fill="x")
        form_frame.grid_columnconfigure(0, weight=0)
        form_frame.grid_columnconfigure(1, weight=1)
        form_frame.grid_columnconfigure(2, weight=0)
        form_frame.grid_columnconfigure(3, weight=1)

        ttkb.Label(form_frame, text="Nombre").grid(row=0, column=0, sticky="w", padx=(0, 10), pady=(0, 16))
        self.tr_nombre = ttkb.Entry(form_frame, width=30)
        self.tr_nombre.grid(row=0, column=1, sticky="ew", pady=(0, 16))

        ttkb.Label(form_frame, text="Fecha de inicio del tratamiento").grid(row=0, column=2, sticky="w", padx=(20, 10), pady=(0, 16))
        self.tr_fecha_inicio = DateEntry(form_frame, year= 2026)
        self.tr_fecha_inicio.grid(row=0, column=3, sticky="w", pady=(0, 16))

        ttkb.Label(form_frame, text="Fecha de final del tratamiento").grid(row=1, column=0, sticky="w", padx=(0, 10), pady=(0, 16))
        self.tr_fecha_final = DateEntry(form_frame, year= 2026)
        self.tr_fecha_final.grid(row=1, column=1, sticky="w", pady=(0, 16))

        ttkb.Label(form_frame, text="Descripción").grid(row=2, column=0, sticky="nw", padx=(0, 10), pady=(0, 16))
        tr_descripcion = tk.Text(form_frame, height=4, width=40)
        tr_descripcion.grid(row=2, column=1, columnspan=3, sticky="ew", pady=(0, 16))


class CrearEventosMongo:
    def __init__(self, parent=None, titulo="Crear", usuario=None):
        self.frame = ttkb.Frame(parent)
        self.frame.pack(fill="both", expand=True)
        self.tabla = "consultas"
        self.usuario = usuario or {}

        self.etiqueta = ttkb.Label(
            self.frame,
            text=f"{titulo} eventos",
            font=("Arial", 14, "bold")
        )
        self.etiqueta.pack(pady=(40, 30))

        botones_frame = ttkb.Frame(self.frame)
        botones_frame.pack(pady=(10, 35), padx=20, fill="x")
        botones_frame.grid_columnconfigure(0, weight=1)
        botones_frame.grid_columnconfigure(1, weight=1)
        botones_frame.grid_columnconfigure(2, weight=1)

        ttkb.Button(
            botones_frame,
            text="Cancelar",
            command=self.ir_lista,
            bootstyle="secondary",
        ).grid(row=0, column=0, sticky="ew", padx=6)
        ttkb.Button(
            botones_frame,
            text="Limpiar campos",
            command=self.limpiar,
            bootstyle="warning",
        ).grid(row=0, column=1, sticky="ew", padx=6)
        ttkb.Button(
            botones_frame,
            text="Guardar cambios",
            command=self.guardar,
            bootstyle="primary",
        ).grid(row=0, column=2, sticky="ew", padx=6)

        form_frame = ttkb.Frame(self.frame)
        form_frame.pack(padx=20, pady=(20, 30), fill="x")
        form_frame.grid_columnconfigure(0, weight=0)
        form_frame.grid_columnconfigure(1, weight=1)
        form_frame.grid_columnconfigure(2, weight=0)
        form_frame.grid_columnconfigure(3, weight=1)

        ttkb.Label(form_frame, text="id").grid(row=0, column=0, sticky="w", padx=(0, 10), pady=(0, 16))
        self.id = ttkb.Entry(form_frame, width=30)
        self.id.insert(0, "6a52e54d9f004e0c00499e17")
        self.id.grid(row=0, column=1, sticky="ew", pady=(0, 16))

        ttkb.Label(form_frame, text="id_tr").grid(row=0, column=2, sticky="w", padx=(20, 10), pady=(0, 16))
        self.id_tr = ttkb.Entry(form_frame, width=30)
        self.id_tr.insert(0, "Llave foranea de tratamientos")
        self.id_tr.grid(row=0, column=3, sticky="ew", pady=(0, 16))

        ttkb.Label(form_frame, text="re_estado").grid(row=1, column=0, sticky="w", padx=(0, 10), pady=(0, 16))
        self.re_estado = ttk.Combobox(
            form_frame,
            values=["Pendiente", "Completado", "Cancelado"],
            state="readonly",
            width=27,
        )
        self.re_estado.set("Pendiente")
        self.re_estado.grid(row=1, column=1, sticky="ew", pady=(0, 16))

        ttkb.Label(form_frame, text="re_titulo").grid(row=1, column=2, sticky="w", padx=(20, 10), pady=(0, 16))
        self.re_titulo = ttkb.Entry(form_frame, width=30)
        self.re_titulo.insert(0, "Título de la consulta")
        self.re_titulo.grid(row=1, column=3, sticky="ew", pady=(0, 16))

        ttkb.Label(form_frame, text="re_fecha").grid(row=2, column=0, sticky="w", padx=(0, 10), pady=(0, 16))
        self.re_fecha = DateEntry(form_frame, year=2020)
        self.re_fecha.set_date("2020-07-11")
        self.re_fecha.grid(row=2, column=1, sticky="w", pady=(0, 16))

        ttkb.Label(form_frame, text="re_hora_inicio").grid(row=2, column=2, sticky="w", padx=(20, 10), pady=(0, 16))
        self.re_hora_inicio = ttkb.Entry(form_frame, width=30)
        self.re_hora_inicio.insert(0, "15:00")
        self.re_hora_inicio.grid(row=2, column=3, sticky="ew", pady=(0, 16))

        ttkb.Label(form_frame, text="re_hora_fin").grid(row=3, column=0, sticky="w", padx=(0, 10), pady=(0, 16))
        self.re_hora_fin = ttkb.Entry(form_frame, width=30)
        self.re_hora_fin.insert(0, "15:05")
        self.re_hora_fin.grid(row=3, column=1, sticky="ew", pady=(0, 16))

        ttkb.Label(form_frame, text="re_observaciones").grid(row=3, column=2, sticky="nw", padx=(20, 10), pady=(0, 16))
        self.re_observaciones = tk.Text(form_frame, height=4, width=40)
        self.re_observaciones.insert("1.0", "Escribe aquí las observaciones")
        self.re_observaciones.grid(row=3, column=3, sticky="ew", pady=(0, 16))

    def limpiar(self):
        limpiar_frame(self.frame)

    def ir_lista(self):
        navegar_a_pagina(self.frame, "Lista eventos", usuario=self.usuario)

    def guardar_valores(self):
        self.nuevo_registro = {
            "id": self.id.get().strip(),
            "id_tr": self.id_tr.get().strip(),
            "re_estado": self.re_estado.get().strip() or "Pendiente",
            "re_observaciones": self.re_observaciones.get("1.0", tk.END).strip(),
            "re_titulo": self.re_titulo.get().strip(),
            "re_hora_fin": self.re_hora_fin.get().strip(),
            "re_hora_inicio": self.re_hora_inicio.get().strip(),
            "re_fecha": self.re_fecha.get_date().strftime("%Y-%m-%d"),
            "re_activo": True,
        }

        if not self.nuevo_registro["id"]:
            del self.nuevo_registro["id"]

    def crear_evento(self):
        self.guardar_valores()
        insertar_registro(self.tabla, self.nuevo_registro)
        messagebox.showinfo("Crear", "Se creó correctamente el evento")
        navegar_a_pagina(self.frame, "Lista eventos", usuario=self.usuario)

    def guardar(self):
        self.crear_evento()
        