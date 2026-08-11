from datetime import datetime
import tkinter as tk
import ttkbootstrap as ttkb
from tkinter import ttk
from tkcalendar import DateEntry
from tkinter import messagebox
from herramients import navegar_a_pagina, limpiar_frame, agregar_boton_mostrar_contrasena, validar_widget, validar_combo
from db.db_mysql import insertar_registro
from seguridad import encriptar_contrasena


class CrearUsuario:
    """Muestra un formulario para crear un nuevo usuario.
    Permite capturar los datos principales y guardarlos en la aplicación."""

    def __init__(self, parent, titulo="Crear", usuario={}):
        """Inicializa la vista de creación del usuario.
        Carga los campos del formulario y prepara los botones de acción."""
        self.frame = ttkb.Frame(parent)
        self.accion = titulo
        self.frame.pack(fill="both", expand=True)
        self.tabla = "usuarios"
        self.usuario = usuario
        self.tipo_usuario = usuario.get("us_tipo_usuario", "")
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
        form_frame.grid_columnconfigure(4, weight=0)

        opciones_tipo_usuario = ["Doctor", "Enfermera"]
        if self.tipo_usuario == "Administrador":
            opciones_tipo_usuario.append("Administrador")

        ttkb.Label(
            form_frame, text="Tipo de usuario *").grid(
            row=0, column=0, sticky="w", padx=(
                0, 10), pady=(
                0, 16))
        self.us_tipo_usuario = tk.StringVar(value="ninguno")
        self.combo_tipo_usuario = ttk.Combobox(
            form_frame,
            textvariable=self.us_tipo_usuario,
            state="readonly",
            width=27,
            values=opciones_tipo_usuario
        )
        self.combo_tipo_usuario.grid(
            row=0, column=1, sticky="ew", pady=(0, 16))

        ttkb.Label(
            form_frame, text="Correo electrónico *").grid(
            row=0, column=2, sticky="w", padx=(
                20, 10), pady=(
                0, 16))
        self.us_correo_electronico = ttkb.Entry(form_frame, width=30)
        self.us_correo_electronico.grid(
            row=0, column=3, sticky="ew", pady=(0, 16))

        ttkb.Label(
            form_frame,
            text="Nombre *").grid(
            row=1,
            column=0,
            sticky="w",
            padx=(
                0,
                10),
            pady=(
                0,
                16))
        self.us_nombre = ttkb.Entry(form_frame, width=30)
        self.us_nombre.grid(row=1, column=1, sticky="ew", pady=(0, 16))

        ttkb.Label(
            form_frame,
            text="Contraseña *").grid(
            row=1,
            column=2,
            sticky="w",
            padx=(
                20,
                10),
            pady=(
                0,
                16))
        self.us_contra = ttkb.Entry(form_frame, width=30, show="*")
        self.us_contra.grid(row=1, column=3, sticky="ew", pady=(0, 16))
        self.btn_mostrar_contra, self.mostrar_contra = agregar_boton_mostrar_contrasena(
            form_frame, self.us_contra, row=1, column=4, sticky="w", padx=(
                6, 0), pady=(
                0, 16), width=3, )

        ttkb.Label(
            form_frame,
            text="Apellidos *").grid(
            row=2,
            column=0,
            sticky="w",
            padx=(
                0,
                10),
            pady=(
                0,
                16))
        self.us_apellidos = ttkb.Entry(form_frame, width=30)
        self.us_apellidos.grid(row=2, column=1, sticky="ew", pady=(0, 16))

        ttkb.Label(
            form_frame,
            text="Cédula *").grid(
            row=2,
            column=2,
            sticky="w",
            padx=(
                20,
                10),
            pady=(
                0,
                16))
        self.us_cedula = ttkb.Entry(form_frame, width=30)
        self.us_cedula.grid(row=2, column=3, sticky="ew", pady=(0, 16))

        ttkb.Label(
            form_frame,
            text="Teléfono *").grid(
            row=3,
            column=2,
            sticky="w",
            padx=(
                20,
                10),
            pady=(
                0,
                16))
        self.us_telefono = ttkb.Entry(form_frame, width=30)
        self.us_telefono.grid(row=3, column=3, sticky="ew", pady=(0, 16))

        ttkb.Label(
            form_frame, text="Fecha de nacimiento").grid(
            row=3, column=0, sticky="w", padx=(
                0, 10), pady=(
                0, 16))
        self.us_fecha_nacimiento = DateEntry(form_frame, year=2026)
        self.us_fecha_nacimiento.grid(
            row=3, column=1, sticky="w", pady=(0, 16))

        ttkb.Label(
            form_frame,
            text="Dirección").grid(
            row=4,
            column=2,
            sticky="w",
            padx=(
                20,
                10),
            pady=(
                0,
                16))
        self.us_direccion = ttkb.Entry(form_frame, width=30)
        self.us_direccion.grid(row=4, column=3, sticky="ew", pady=(0, 16))

        especialidades_medicas = [
            "Geriatria",
            "Cardiología",
            "Dermatología",
            "Neurología",
            "Pediatría",
            "Psiquiatría",
            "Oncología",
            "Gastroenterología",
            "Neumología",
            "Endocrinología",
            "Oftalmología"
        ]
        ttkb.Label(
            form_frame, text="Especialidad").grid(
            row=4, column=0, sticky="w", padx=(
                0, 10), pady=(
                0, 16))
        self.us_especialidad = tk.StringVar(value="ninguno")
        self.combo_especialidad = ttk.Combobox(
            form_frame,
            textvariable=self.us_especialidad,
            state="readonly",
            width=27,
            values=especialidades_medicas
        )
        self.combo_especialidad.grid(
            row=4, column=1, sticky="ew", pady=(0, 16))

    def limpiar(self):
        """Limpia los campos del formulario para empezar de nuevo."""
        limpiar_frame(self.frame)

    def ir_lista(self):
        """Regresa a la vista de lista de usuarios."""
        navegar_a_pagina(
            self.frame,
            f"Lista {
                self.tabla}",
            usuario=self.usuario)

    def guardar_valores(self):
        """Recoge la información ingresada en los campos del formulario.
        Convierte esos datos en un diccionario listo para guardar."""
        # actualizar los valores del diccionario con los valores de lo widgets
        self.nuevo_registro = {
            'us_tipo_usuario': '',
            'us_nombre': '',
            'us_apellidos': '',
            'us_fecha_nacimiento': "1980-01-01",
            'us_cedula': '',
            'us_telefono': '',
            'us_correo_electronico': '',
            'us_direccion': '',
            'us_especialidad': ''}

        # encryptar contraseña solo si la actualizaron
        if self.us_contra.get() != "":
                self.nuevo_registro.update({"us_contraseña": encriptar_contrasena(
                    self.us_contra.get())})  
        self.nuevo_registro["us_tipo_usuario"] = self.us_tipo_usuario.get()
        self.nuevo_registro["us_nombre"] = self.us_nombre.get()
        self.nuevo_registro["us_apellidos"] = self.us_apellidos.get()
        self.nuevo_registro["us_fecha_nacimiento"] = self.us_fecha_nacimiento.get_date(
        ).strftime("%Y-%m-%d")
        self.nuevo_registro["us_telefono"] = self.us_telefono.get()
        self.nuevo_registro["us_cedula"] = self.us_cedula.get()
        self.nuevo_registro["us_correo_electronico"] = self.us_correo_electronico.get(
        )
        self.nuevo_registro["us_direccion"] = self.us_direccion.get()
        self.nuevo_registro["us_especialidad"] = self.us_especialidad.get()

    def crear_usuario(self):
        """Valida la información ingresada y guarda el nuevo usuario.
        Si falta algún dato importante, muestra un mensaje y no continúa."""
        if not validar_combo(self.us_tipo_usuario, "Tipo de usuario"): return
        if not validar_widget(self.us_nombre, "Nombre", max_len=50): return
        if not validar_widget(self.us_apellidos, "Apellidos", max_len=50): return
        if not validar_widget(self.us_contra, "Contraseña", max_len=255, min_len=6): return
        if not validar_widget(self.us_correo_electronico, "Correo", max_len=50): return
        if not validar_widget(self.us_cedula, "Cédula", max_len=11, tipo="numerico"): return
        if not validar_widget(self.us_telefono, "Teléfono", max_len=10, tipo="numerico"): return
        if not validar_widget(self.us_direccion, "Dirección", max_len=200, requerido=False): return
        correo = self.us_correo_electronico.get().strip()
        if "@" not in correo or ".com" not in correo:
            messagebox.showerror("Correo inválido", "El correo debe contener '@' y '.com'")
            return
        fecha_nac = self.us_fecha_nacimiento.get_date()
        if fecha_nac.year < 1926:
            messagebox.showerror("Fecha inválida",
                                 "La fecha de nacimiento debe ser de 1926 en adelante")
            return
        self.guardar_valores()
        insertar_registro(self.tabla, self.nuevo_registro)

        messagebox.showinfo("Crear", "Se creó correctamente el usuario")
        navegar_a_pagina(self.frame, "Lista usuarios", usuario=self.usuario)

    def guardar(self):
        """Ejecuta la creación del usuario desde el botón guardar."""
        self.crear_usuario()
