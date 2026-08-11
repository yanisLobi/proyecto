import tkinter as tk
import ttkbootstrap as ttkb
from tkinter import ttk
from tkinter import messagebox
from typing import Any, cast
from herramients import mostrar_sin_registros, navegar_a_pagina, obtener_columnas, regresar_string
from db.db_mysql import obtener_registros, obtener_tabla, borrar_registro, obtener_tratamientos_enfermera, obtener_valores


class ListaTratamientos:
    """Muestra la lista de registros en una tabla interactiva.
    Permite ver, eliminar y navegar a otras pantallas según el tipo de usuario."""

    def __init__(self, parent, usuario={}):
        """Inicializa la vista de lista con los botones y la tabla de registros.
        parent es el contenedor de la interfaz y usuario guarda la sesión actual."""

        self.tabla = 'tratamientos'
        self.usuario = usuario
        self.frame = ttkb.Frame(parent)
        self.frame.pack(fill="both", expand=True)
        self.boton_actualizar = None
        self.boton_eliminar = None
        self.tipo_usuario = usuario.get("us_tipo_usuario")
        if self.tipo_usuario in ["Doctor", "Administrador"]:
            botones_frame = ttkb.Frame(self.frame)
            botones_frame.pack(pady=(40, 45), padx=20, fill="x")
            botones_frame.grid_columnconfigure(0, weight=1)
            botones_frame.grid_columnconfigure(1, weight=1)
            botones_frame.grid_columnconfigure(2, weight=1)

            ttkb.Button(
                botones_frame,
                text=f"Crear {self.tabla.title()}",
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
            text=f"lista de {self.tabla}",
            font=("Arial", 14, "bold")
        )
        self.etiqueta.pack(pady=(40, 30))

        self.id_usuario = usuario.get("id_usuarios")
        lista_tratamiento = obtener_tabla(self.tabla, solo_activos=False)

        # Si no hay registros, evitar error con self.lista_tratamiento[0]
        if not lista_tratamiento:
            mostrar_sin_registros(self.frame, self.tabla)
            return

        tratamiento = cast(dict[str, Any], lista_tratamiento[0])

        self.columnas = obtener_columnas(tratamiento.keys(), self.tipo_usuario)
        self.columnas_tupla = tuple(self.columnas)

        self.tree = ttk. Treeview(
            self.frame,
            columns=self.columnas_tupla,
            show="headings")
        ancho_columna = int(1000 / len(self.columnas))
        for columna in self.columnas:

            self.tree.heading(
                columna,
                text=regresar_string(columna),
                anchor="center")
            self.tree.column(
                columna,
                width=ancho_columna,
                minwidth=30,
                stretch=False,
                anchor="center")

        # Mapear la foreign key con la pagina que se abre cuando le damos doble
        # clic
        self.fk_paginas = {
            "id_paciente": "Actualizar pacientes",
            "id_doctor": "Actualizar usuarios",
        }

        # Mapas para mostrar nombres en lugar de IDs
        self.fk_display_map = {
            "id_paciente": self._cargar_display_map_pacientes(),
            "id_doctor": self._cargar_display_map_usuarios(),
        }
        # Guardar el id real por fila/columna (porque en la tabla se mostrará
        # el nombre)
        self.fk_ids_por_fila = {}

        self.recargar_tabla()
        self.tree.bind("<<TreeviewSelect>>", self.on_seleccion)
        self.on_seleccion()

        self.tree.pack(pady=(10, 0))

    def recargar_tabla(self):
        """Actualiza la información mostrada en la tabla según el usuario actual.
        Carga los registros disponibles y los muestra en la vista."""

        if self.tipo_usuario == "Doctor":
            lista_registros = obtener_registros(
                self.tabla, "id_doctor", self.id_usuario)
        elif self.tipo_usuario == "Administrador":
            lista_registros = obtener_tabla(self.tabla, solo_activos=False)
        else:  # Enfermeras
            lista_registros = obtener_tratamientos_enfermera(self.id_usuario)

        # limpiar filas
        for item in self.tree.get_children():
            self.tree.delete(item)

        self.fk_ids_por_fila = {}
        # llenar tabla
        for registro in lista_registros:
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
        """Abre la pantalla para crear un nuevo registro.
        Cambia de vista y pasa el usuario activo como contexto."""
        navegar_a_pagina(
            self.frame,
            f"Crear {
                self.tabla}",
            usuario=self.usuario)

    def on_seleccion(self, event=None):
        """Activa o desactiva los botones de acción según haya una fila seleccionada.
        Esto evita ejecutar acciones sin un registro elegido."""
        if self.boton_actualizar is None and self.boton_eliminar is None:
            return
        estado = "normal" if self.tree.selection() else "disabled"
        if self.boton_actualizar is not None:
            self.boton_actualizar.config(state=estado)
        if self.boton_eliminar is not None:
            self.boton_eliminar.config(state=estado)

    def obtener_id_seleccionado(self):
        """Devuelve el identificador del registro que está seleccionado.
        Si no hay selección, muestra un mensaje de advertencia."""
        item_id = self.tree.selection()
        if not item_id:
            messagebox.showinfo(
                "Error", f"Debes seleccionar un {
                    self.tabla.title()} de la tabla")
            return

        self.valores = self.tree.item(item_id[0], "values")
        if not self.valores:
            messagebox.showinfo("Error", "La fila seleccionada no tiene datos")
            return

        return self.valores[0]

    def borrar(self):
        """Elimina el registro seleccionado de la lista.
        Usa el identificador actual para borrar el elemento correspondiente."""
        id = self.obtener_id_seleccionado()
        borrar_registro(self.tabla, self.columnas_tupla[0], id)
        messagebox.showinfo(
            "Eliminar", f"Haz eliminado el {
                self.tabla.title()} con ID = {id}")
        self.recargar_tabla()

    def ir_actualizar(self):
        """Abre la pantalla para ver o modificar el registro seleccionado.
        Pasa el identificador del elemento elegido a la siguiente vista."""
        item_id = self.tree.selection()
        if not item_id:
            messagebox.showinfo(
                "Sin selección",
                f"seleccione un {
                    self.tabla} ")

            return

        id = self.obtener_id_seleccionado()
        navegar_a_pagina(
            self.frame,
            f"Actualizar {
                self.tabla}",
            id_seleccionado=id,
            usuario=self.usuario)

    def _cargar_display_map_pacientes(self):
        """Carga un mapa para mostrar nombres de pacientes en lugar de sus identificadores.
        Esto hace más clara la información mostrada en la tabla."""
        try:
            filas = obtener_valores(
                "pacientes",
                "id_pacientes",
                "pa_nombre",
                "pa_apellidos")
        except Exception:
            return {}

        return {str(id_paciente): f"{nombre} {apellido}".strip()
                for id_paciente, nombre, apellido in filas}

    def _cargar_display_map_usuarios(self):
        """Carga un mapa para mostrar nombres de usuarios en lugar de sus identificadores.
        Esto facilita la lectura de la información en la tabla."""
        try:
            filas = obtener_valores(
                "usuarios",
                "id_usuarios",
                "us_nombre",
                "us_apellidos")
        except Exception:
            return {}

        return {str(id_us): f"{nombre} {apellido}".strip()
                for id_us, nombre, apellido in filas}
