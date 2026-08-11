from datetime import datetime
import tkinter as tk
import ttkbootstrap as ttkb
from tkinter import ttk
from tkcalendar import DateEntry
from tkinter import messagebox
from herramients import navegar_a_pagina, limpiar_frame, validar_widget, validar_combo
from db.db_mysql import insertar_registro, obtener_valores_usuarios


class CrearPacientes:
    """Muestra un formulario para crear un nuevo registro (este mismo constructor se usa en Actualizar).
    Permite ingresar los datos básicos y guardarlos en la base de datos."""

    def __init__(self, parent, titulo="Crear", usuario={}):
        """Inicializa el formulario de creación de pacientes.
        parent es el contenedor donde se dibuja la ventana y usuario guarda la sesión actual."""

        self.frame = ttkb.Frame(parent)
        self.frame.pack(fill="both", expand=True)
        self.tabla = "pacientes"
        self.usuario = usuario
        self.tipo_usuario = usuario.get("us_tipo_usuario")
        self.etiqueta = ttkb.Label(
            self.frame,
            text=f"{titulo} {self.tabla} ",
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
       
        if self.tipo_usuario in ["Doctor", "Administrador"]:
            ttkb.Button(
                        botones_frame,
                        text="Limpiar campos",
                        command=self.limpiar,
                        bootstyle="warning",
                    ).grid(row=0, column=1, sticky="ew", padx=6)
             
            ttkb.Button(
                botones_frame,
                text="Guardar",
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
            form_frame,
            text="Nombre *").grid(
            row=0,
            column=0,
            sticky="w",
            padx=(
                0,
                10),
            pady=(
                0,
                16))
        self.pa_nombre = ttkb.Entry(form_frame, width=30)
        self.pa_nombre.grid(row=0, column=1, sticky="ew", pady=(0, 16))

        ttkb.Label(
            form_frame,
            text="Apellidos *").grid(
            row=0,
            column=2,
            sticky="w",
            padx=(
                20,
                10),
            pady=(
                0,
                16))
        self.pa_apellidos = ttkb.Entry(form_frame, width=30)
        self.pa_apellidos.grid(row=0, column=3, sticky="ew", pady=(0, 16))

        ttkb.Label(
            form_frame, text="Fecha de nacimiento").grid(
            row=1, column=0, sticky="w", padx=(
                0, 10), pady=(
                0, 16))
        self.pa_fecha_nacimiento = DateEntry(form_frame, year=2026)
        self.pa_fecha_nacimiento.grid(
            row=1, column=1, sticky="w", pady=(0, 16))

        ttkb.Label(
            form_frame, text="Telefono del Contacto de emergencia *").grid(
            row=1, column=2, sticky="w", padx=(
                20, 10), pady=(
                0, 16))
        self.pa_tel_contacto_emergencia = ttkb.Entry(form_frame, width=30)
        self.pa_tel_contacto_emergencia.grid(
            row=1, column=3, sticky="ew", pady=(0, 16))

        ttkb.Label(
            form_frame, text="Nombre del contacto de emergencia *").grid(
            row=2, column=0, sticky="w", padx=(
                0, 10), pady=(
                0, 16))
        self.pa_nombre_contacto_emergencia = ttkb.Entry(form_frame, width=30)
        self.pa_nombre_contacto_emergencia.grid(
            row=2, column=1, sticky="ew", pady=(0, 16))
        # columnspan es para definir cuantas seldad de ancho

        ttkb.Label(
            form_frame, text="Enfermera a cargo *").grid(
            row=2, column=2, sticky="w", padx=(
                20, 10), pady=(
                0, 16))
        self.enfermeras = obtener_valores_usuarios(
            "id_usuarios", "us_apellidos", "us_tipo_usuario", "Enfermera")
        self.id_enfermera = tk.StringVar(value="ninguno")
        self.combo_id_enfermera = ttk.Combobox(
            form_frame,
            textvariable=self.id_enfermera,
            state="readonly",
            width=27,
            values=self.enfermeras,
        )
        self.combo_id_enfermera.grid(
            row=2, column=3, sticky="ew", pady=(0, 16))

    def limpiar(self):
        """Limpia los campos del formulario para empezar de nuevo."""
        limpiar_frame(self.frame)

    def ir_lista(self):
        """Regresa a la vista de lista de pacientes.
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
            'pa_nombre': '',
            'pa_apellidos': '',
            'pa_fecha_nacimiento': "1980-01-01",
            'pa_nombre_contacto_emergencia': '',
            'pa_tel_contacto_emergencia': '',
            'id_enfermera_principal': '',


        }

        self.nuevo_registro["pa_nombre"] = self.pa_nombre.get()
        self.nuevo_registro["pa_apellidos"] = self.pa_apellidos.get()
        self.nuevo_registro["pa_fecha_nacimiento"] = self.pa_fecha_nacimiento.get_date(
        ).strftime("%Y-%m-%d")
        self.nuevo_registro["pa_nombre_contacto_emergencia"] = self.pa_nombre_contacto_emergencia.get(
        )
        self.nuevo_registro["pa_tel_contacto_emergencia"] = self.pa_tel_contacto_emergencia.get(
        )
        self.nuevo_registro["id_enfermera_principal"] = self.id_enfermera.get(
        ).split()[0]  # sirve para sacar el id, dentro de muchos valores

    def crear_paciente(self):
        """Ejecuta todas las validaciones de widgets y guarda el nuevo paciente.
        Si falta información importante, muestra un mensaje de error y se detiene el metodo"""
        if not validar_widget(self.pa_nombre, "Nombre", max_len=50): return
        if not validar_widget(self.pa_apellidos, "Apellidos", max_len=50): return
        if not validar_widget(self.pa_nombre_contacto_emergencia, "Nombre contacto emergencia", max_len=50): return
        if not validar_widget(self.pa_tel_contacto_emergencia, "Teléfono contacto", max_len=10, tipo="numerico"): return
        if not validar_combo(self.id_enfermera, "Enfermera a cargo"): return
        self.guardar_valores()
        insertar_registro(self.tabla, self.nuevo_registro)

        messagebox.showinfo("Crear", "Se creó correctamente el paciente")
        navegar_a_pagina(self.frame, "Lista pacientes", usuario=self.usuario)
        # messabox, se actualizo correctamente.
        # regresar a lista usuarios

    def guardar(self):
        """Ejecuta la creación del paciente desde el botón guardar."""
        self.crear_paciente()
