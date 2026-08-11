import tkinter as tk
import ttkbootstrap as ttkb
from tkinter import ttk
from tkinter import messagebox
from typing import Any, cast

from herramients import navegar_a_pagina, regresar_string, mostrar_sin_registros
from db.db_mongo import (
    obtener_eventos_doctor,
    obtener_eventos_enfermera,
    obtener_tabla,
    borrar_registro
   
)
from db.db_mysql import obtener_tabla as obtener_tabla_mysql


class ListaEventos:
    """Muestra una vista básica de recordatorios en pantalla."""

    def __init__(self, parent):
        """Inicializa el encabezado de la vista de recordatorios."""
        self.frame = ttkb.Frame(parent)
        self.frame.pack(fill="both", expand=True)

        self.etiqueta = ttkb.Label(
            self.frame,
            text="Lista de recordatorios",
            font=("Arial", 14, "bold")
        )
        self.etiqueta.pack(pady=20)


class ListaEventosMongo:
    """Muestra la lista principal de recordatorios en una tabla interactiva.
    Permite crear, eliminar, revisar y navegar según el tipo de usuario."""

    def __init__(self, parent, usuario=None):
        """Inicializa la vista de lista con los controles y la tabla de datos.
        Recibe el contenedor principal y la información del usuario activo."""
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
                text="Crear Recordatorios",
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
            text="lista de recordatorios",
            font=("Arial", 14, "bold")
        )
        self.etiqueta.pack(pady=(40, 30))

        self.columnas_tupla = (
            "id",
            "id_tr",
            "re_estado",
            "re_observaciones",
            "re_titulo",
            "re_hora_inicio",
            "re_hora_fin",
            "re_fecha",
            "re_autor",
            "re_frecuencia",
            "re_medicamento"
        )

        self.tree = ttk.Treeview(
            self.frame,
            columns=self.columnas_tupla,
            show="headings")
        ancho_columna = int(1100 / len(self.columnas_tupla))
        for columna in self.columnas_tupla:
            self.tree.heading(
                columna,
                text=regresar_string(columna),
                anchor="center")
            self.tree.column(
                columna,
                width=ancho_columna,
                minwidth=50,
                stretch=False,
                anchor="center")

        self.fk_paginas = {
            "id_tr": "Actualizar tratamientos",
        }
        self.fk_display_map = {
            "id_tr": self._cargar_display_map_tratamientos(),
        }
        self.fk_ids_por_fila = {}

        self.recargar_tabla()
        self.tree.bind("<<TreeviewSelect>>", self.on_seleccion)
        self.on_seleccion()
        self.tree.pack(pady=(10, 0))

    def recargar_tabla(self):
        """Actualiza la información visible en la tabla de recordatorios."""
        for item in self.tree.get_children():
            self.tree.delete(item)

        if self.tipo_usuario == "Doctor":
            registros = obtener_eventos_doctor(self.usuario.get("id_usuarios"))
        elif self.tipo_usuario == "Enfermera":
            registros = obtener_eventos_enfermera(self.usuario.get("id_usuarios"))
        else:
            registros = obtener_tabla(self.tabla)

        self.fk_ids_por_fila = {}
        for registro in registros:
            registro = cast(dict[str, Any], registro)
            valores = []
            fk_ids = {}

            for col in self.columnas_tupla:
                val = registro.get(col)
                if col in self.fk_paginas:
                    fk_ids[col] = val
                    display = self.fk_display_map.get(col, {}).get(str(val))
                    if display is None:
                        display = str(val) if val is not None else ""
                    valores.append(display)
                else:
                    valores.append(val)

            iid = self.tree.insert("", tk.END, values=tuple(valores))
            self.fk_ids_por_fila[iid] = fk_ids

        self.on_seleccion()

    def ir_crear(self):
        """Abre la pantalla para crear un nuevo recordatorio."""
        navegar_a_pagina(self.frame, "Crear eventos", usuario=self.usuario)

    def on_seleccion(self, event=None):
        """Activa o desactiva los botones según haya una fila seleccionada."""
        if self.boton_actualizar is None and self.boton_eliminar is None:
            return

        estado = "normal" if self.tree.selection() else "disabled"
        if self.boton_actualizar is not None:
            self.boton_actualizar.config(state=estado)
        if self.boton_eliminar is not None:
            self.boton_eliminar.config(state=estado)

    def obtener_id_seleccionado(self):
        """Devuelve el identificador del recordatorio seleccionado."""
        item_id = self.tree.selection()
        if not item_id:
            messagebox.showinfo(
                "Error", "Debes seleccionar un recordatorio de la tabla")
            return None

        valores = self.tree.item(item_id[0], "values")
        if not valores:
            messagebox.showinfo("Error", "La fila seleccionada no tiene datos")
            return None

        return str(valores[0])

    def borrar(self):
        """Elimina el recordatorio seleccionado de la lista."""
        id_seleccionado = self.obtener_id_seleccionado()
        if not id_seleccionado:
            return

        borrar_registro(self.tabla, "id", id_seleccionado)
        messagebox.showinfo(
            "Eliminar",
            f"Haz eliminado el recordatorio con ID = {id_seleccionado}")
        self.recargar_tabla()

    def ir_actualizar(self):
        """Abre la vista para revisar o modificar el recordatorio elegido."""
        id_seleccionado = self.obtener_id_seleccionado()
        if not id_seleccionado:
            return

        navegar_a_pagina(
            self.frame,
            "Actualizar eventos",
            id_seleccionado=id_seleccionado,
            usuario=self.usuario,
        )

    def _cargar_display_map_tratamientos(self):
        """Construye un mapa de texto para mostrar mejor los tratamientos.
        Combina nombres relacionados para que la tabla sea más legible."""
        try:
            tratamientos = obtener_tabla_mysql(
                "tratamientos", solo_activos=False)
            pacientes = obtener_tabla_mysql("pacientes", solo_activos=False)
            mapa_pacientes = {
                str(p.get("id_pacientes", "")): f"{p.get('pa_nombre', '')} {p.get('pa_apellidos', '')}".strip()
                for p in pacientes
            }
            resultado = {}
            for tr in tratamientos:
                id_tr = str(tr.get("id_tratamientos", ""))
                nombre_tr = str(tr.get("tr_nombre", ""))
                id_pac = str(tr.get("id_paciente", ""))
                nombre_pac = mapa_pacientes.get(id_pac, "")
                resultado[id_tr] = f"{nombre_tr} - {nombre_pac}" if nombre_pac else nombre_tr
            return resultado
        except Exception:
            return {}

    def obtener_celda_evento(self, event):
        """Devuelve la celda seleccionada en la tabla a partir del clic del usuario."""
        region = self.tree.identify_region(event.x, event.y)
        if region != "cell":
            return None

        row_id = self.tree.identify_row(event.y)
        col_id = self.tree.identify_column(event.x)
        if not row_id or not col_id:
            return None

        try:
            col_index = int(col_id.lstrip("#")) - 1
        except ValueError:
            return None

        if col_index < 0 or col_index >= len(self.columnas_tupla):
            return None

        col_name = self.columnas_tupla[col_index]
        values = self.tree.item(row_id, "values")
        if not values:
            return None

        return row_id, col_name, values[col_index]
