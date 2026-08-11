import tkinter as tk
import ttkbootstrap as ttkb
from tkinter import messagebox
from tkcalendar import DateEntry
from tkinter import ttk
from tkcalendar import DateEntry
from herramients import navegar_a_pagina, limpiar_frame, validar_widget, validar_combo
from db.db_mysql import insertar_registro


class CrearMedicamentos:
    """Muestra un formulario para crear un nuevo registro.
    Permite ingresar los datos básicos y guardarlos en la base de datos."""

    def __init__(self, parent=None, usuario={}, titulo="Crear"):
        """Inicializa la vista de creación.
        Carga el formulario y prepara los controles para recibir la información."""
        # me queda la duda de que es parent
        self.frame = ttkb.Frame(parent)
        self.frame.pack(fill="both", expand=True)
        self.tabla = 'medicamentos'
        self.usuario = usuario
        self.tipo_usuario = usuario.get("us_tipo_usuario")
        self.etiqueta = ttkb.Label(
            self.frame,
            text=f"{titulo} {self.tabla}",
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

        ttkb.Label(
            form_frame, text="Nombre comercial *").grid(
            row=0, column=0, sticky="w", padx=(
                0, 10), pady=(
                0, 16))
        self.me_nombre_comercial = ttkb.Entry(form_frame, width=30)
        self.me_nombre_comercial.grid(
            row=0, column=1, sticky="ew", pady=(0, 16))

        ttkb.Label(
            form_frame, text="Forma farmacéutica *").grid(
            row=0, column=2, sticky="w", padx=(
                20, 10), pady=(
                0, 16))
        self.me_forma_farmaceutica = tk.StringVar(value="ninguno")
        self.combo_forma_framaceutica = ttk.Combobox(
            form_frame,
            textvariable=self.me_forma_farmaceutica,
            state="readonly",
            width=27,
            values=["Sólidas", "Semisólidas", "Líquidas", "Inhalables"]
        )
        self.combo_forma_framaceutica.grid(
            row=0, column=3, sticky="ew", pady=(0, 16))

        ttkb.Label(
            form_frame, text="Concentración *").grid(
            row=1, column=0, sticky="w", padx=(
                0, 10), pady=(
                0, 16))
        self.me_concentracion = ttkb.Entry(form_frame, width=30)
        self.me_concentracion.grid(row=1, column=1, sticky="ew", pady=(0, 16))

        ttkb.Label(
            form_frame, text="Fecha de caducidad").grid(
            row=1, column=2, sticky="w", padx=(
                20, 10), pady=(
                0, 16))
        self.me_fecha_caducidad = DateEntry(form_frame, year=2026)
        self.me_fecha_caducidad.grid(row=1, column=3, sticky="w", pady=(0, 16))

        ttkb.Label(
            form_frame, text="Descripción").grid(
            row=2, column=0, sticky="nw", padx=(
                0, 10), pady=(
                0, 16))
        self.me_descripcion = tk.Text(form_frame, width=40, height=4)
        self.me_descripcion.grid(row=2, column=1, sticky="ew", pady=(0, 16))

    def limpiar(self):
        """Limpia los campos del formulario para empezar de nuevo."""
        limpiar_frame(self.frame)

    def ir_lista(self):
        """Regresa a la vista de lista.
        Cambia de pantalla usando la navegación de la aplicación."""
        navegar_a_pagina(
            self.frame,
            f"Lista {
                self.tabla}",
            usuario=self.usuario)

    def guardar_valores(self):
        """Recoge los datos escritos en los campos del formulario.
        Convierte esa información en un diccionario listo para guardarse en la base de datos."""
        # actualizar los valores del diccionario con los valores de lo widgets
        self.nuevo_registro = {
            'me_nombre_comercial': '',
            'me_forma_farmaceutica': '',
            'me_concentracion': '',
            'me_fecha_caducidad': "1980-01-01",
            'me_descripcion': ''
        }

        self.nuevo_registro["me_nombre_comercial"] = self.me_nombre_comercial.get(
        )
        self.nuevo_registro["me_forma_farmaceutica"] = self.me_forma_farmaceutica.get(
        )
        self.nuevo_registro["me_concentracion"] = self.me_concentracion.get()
        self.nuevo_registro["me_fecha_caducidad"] = self.me_fecha_caducidad.get_date(
        ).strftime("%Y-%m-%d")
        self.nuevo_registro["me_descripcion"] = self.me_descripcion.get(
            "1.0", "end-1c")

    def crear_medicamentos(self):
        """Valida la información ingresada y guarda el nuevo registro.
        Si falta algo importante, muestra un mensaje y no continúa."""
        if not validar_widget(self.me_nombre_comercial, "Nombre comercial", max_len=50): return
        if not validar_widget(self.me_concentracion, "Concentración", max_len=50): return
        if not validar_widget(self.me_descripcion, "Descripción", max_len=100, requerido=False): return
        if not validar_combo(self.me_forma_farmaceutica, "Forma farmacéutica"): return
        self.guardar_valores()
        insertar_registro(self.tabla, self.nuevo_registro)

        messagebox.showinfo("Crear", "Se creó correctamente el medicamento")
        navegar_a_pagina(
            self.frame,
            f"Lista {
                self.tabla}",
            usuario=self.usuario)
        # messabox, se actualizo correctamente.
        # regresar a lista usuarios

    def guardar(self):
        """Ejecuta la creación desde el botón guardar."""
        self.crear_medicamentos()
