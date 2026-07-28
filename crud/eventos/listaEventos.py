import tkinter as tk
import ttkbootstrap as ttkb
from tkinter import ttk
from tkinter import messagebox

from herramients import navegar_a_pagina_mongo as navegar_a_pagina, regresar_string
from db_mongo import obtener_tabla, borrar_registro


class ListaEventos:
    def __init__(self, parent):
        self.frame = ttkb.Frame(parent)
        self.frame.pack(fill="both", expand=True)

        self.etiqueta = ttkb.Label(
            self.frame,
            text="Lista de pacientes",
            font=("Arial", 14, "bold")
        )
        self.etiqueta.pack(pady=20)


class ListaEventosMongo:
    def __init__(self, parent, usuario=None):
        self.tabla = "consultas"
        self.frame = ttkb.Frame(parent)
        self.frame.pack(fill="both", expand=True)
        self.usuario = usuario or {}
        self.tipo_usuario = self.usuario.get("us_tipo_usuario")

        self.boton_actualizar = None
        self.boton_eliminar = None

        if self.tipo_usuario in ["Doctor", "Administrador"]:
            botones_frame = ttkb.Frame(self.frame)
            botones_frame.pack(pady=(40, 45), padx=20, fill="x")
            botones_frame.grid_columnconfigure(0, weight=1)
            botones_frame.grid_columnconfigure(1, weight=1)
            botones_frame.grid_columnconfigure(2, weight=1)

            ttkb.Button(
                botones_frame,
                text="Crear Eventos",
                command=self.ir_crear,
                bootstyle="primary",
            ).grid(row=0, column=0, sticky="ew", padx=6)

            self.boton_eliminar = ttkb.Button(
                botones_frame,
                text="Eliminar",
                command=self.borrar,
                state="disabled",
                bootstyle="danger",
            )
            self.boton_eliminar.grid(row=0, column=1, sticky="ew", padx=6)

            self.boton_actualizar = ttkb.Button(
                botones_frame,
                text="Ver detalles",
                command=self.ir_actualizar,
                state="disabled",
                bootstyle="info",
            )
            self.boton_actualizar.grid(row=0, column=2, sticky="ew", padx=6)

        self.etiqueta = ttkb.Label(
            self.frame,
            text="lista de eventos",
            font=("Arial", 14, "bold")
        )
        self.etiqueta.pack(pady=(40, 30))

        self.columnas_tupla = (
            "id",
            "id_tr",
            "re_estado",
            "re_observaciones",
            "re_titulo",
            "re_hora_fin",
            "re_hora_inicio",
            "re_fecha",
        )

        self.tree = ttk.Treeview(self.frame, columns=self.columnas_tupla, show="headings")
        ancho_columna = int(1100 / len(self.columnas_tupla))
        for columna in self.columnas_tupla:
            self.tree.heading(columna, text=regresar_string(columna), anchor="center")
            self.tree.column(columna, width=ancho_columna, minwidth=50, stretch=False, anchor="center")

        self.recargar_tabla()
        self.tree.bind("<<TreeviewSelect>>", self.on_seleccion)
        self.on_seleccion()
        self.tree.pack(pady=(10, 0))

    def recargar_tabla(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for registro in obtener_tabla(self.tabla):
            valores = tuple(registro.get(col, "") for col in self.columnas_tupla)
            self.tree.insert("", tk.END, values=valores)

        self.on_seleccion()

    def ir_crear(self):
        navegar_a_pagina(self.frame, "Crear eventos", usuario=self.usuario)

    def on_seleccion(self, event=None):
        if self.boton_actualizar is None and self.boton_eliminar is None:
            return

        estado = "normal" if self.tree.selection() else "disabled"
        if self.boton_actualizar is not None:
            self.boton_actualizar.config(state=estado)
        if self.boton_eliminar is not None:
            self.boton_eliminar.config(state=estado)

    def obtener_id_seleccionado(self):
        item_id = self.tree.selection()
        if not item_id:
            messagebox.showinfo("Error", "Debes seleccionar un evento de la tabla")
            return None

        valores = self.tree.item(item_id[0], "values")
        if not valores:
            messagebox.showinfo("Error", "La fila seleccionada no tiene datos")
            return None

        return str(valores[0])

    def borrar(self):
        id_seleccionado = self.obtener_id_seleccionado()
        if not id_seleccionado:
            return

        borrar_registro(self.tabla, "id", id_seleccionado)
        messagebox.showinfo("Eliminar", f"Haz eliminado el evento con ID = {id_seleccionado}")
        self.recargar_tabla()

    def ir_actualizar(self):
        id_seleccionado = self.obtener_id_seleccionado()
        if not id_seleccionado:
            return

        navegar_a_pagina(
            self.frame,
            "Actualizar eventos",
            id_seleccionado=id_seleccionado,
            usuario=self.usuario,
        )