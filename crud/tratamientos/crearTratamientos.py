import tkinter as tk
import ttkbootstrap as ttkb
from tkinter import messagebox
from tkcalendar import DateEntry
from tkinter import ttk
from tkcalendar import DateEntry
from herramients import navegar_a_pagina, limpiar_frame, validar_widget, validar_combo
from db_mysql import insertar_registro, obtener_medicinas_de_tratamientos, obtener_valores, obtener_valores_medicamentos, obtener_valores_usuarios, insertar_receta


class CrearTratamientos:
    def __init__(self, parent=None, titulo="Crear", usuario={}):
        # me queda la duda de que es parent
        self.frame = ttkb.Frame(parent)
        self.frame.pack(fill="both", expand=True)
        self.tabla = 'tratamientos'
        self.usuario = usuario
        self.tipo_usuario = usuario.get("us_tipo_usuario")
        self.etiqueta = ttkb.Label(
            self.frame,
            text=f"{titulo} {self.tabla}",
            font=("Arial", 14, "bold")
        )
        self.etiqueta.pack(pady=(40, 30))

        self.valores_pacientes = obtener_valores(
            "pacientes",
            "id_pacientes",
            "pa_nombre",
            "pa_apellidos",
            solo_activos=True)
        self.valores_medicamentos = obtener_valores_medicamentos(
            "medicamentos", "id_medicamentos", "me_nombre_comercial", solo_activos=True)
        self.valores_doctor = obtener_valores_usuarios(
            "id_usuarios", "us_nombre", "us_apellidos", "Doctor", solo_activos=True)
        valores_enfermera = obtener_valores_usuarios(
            "id_usuarios", "us_nombre", "us_apellidos", "Enfermera")

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
        self.tr_nombre = ttkb.Entry(form_frame, width=30)
        self.tr_nombre.grid(row=0, column=1, sticky="ew", pady=(0, 16))

        ttkb.Label(
            form_frame,
            text="Paciente *").grid(
            row=0,
            column=2,
            sticky="w",
            padx=(
                20,
                10),
            pady=(
                0,
                16))
        self.paciente = self.valores_pacientes
        self.id_paciente = tk.StringVar(value="ninguno")
        self.combo_id_paciente = ttk.Combobox(
            form_frame,
            textvariable=self.id_paciente,
            state="readonly",
            width=27,
            values=self.paciente)
        # self.id_paciente.current(0)
        self.combo_id_paciente.grid(row=0, column=3, sticky="ew", pady=(0, 16))

        ttkb.Label(
            form_frame,
            text="Doctor *").grid(
            row=1,
            column=0,
            sticky="w",
            padx=(
                0,
                10),
            pady=(
                0,
                16))
        
        if self.tipo_usuario == "Administrador":
            self.doctor = self.valores_doctor
            self.id_doctor = tk.StringVar(value="ninguno")
            self.combo_id_doctor = ttk.Combobox(
                form_frame,
                textvariable=self.id_doctor,
                state="readonly",
                width=27,
                values=self.doctor,
            )
            
        # self.id_doctor.current(0)
        self.combo_id_doctor.grid(row=1, column=1, sticky="ew", pady=(0, 16))

        ttkb.Label(
            form_frame, text="Fecha de inicio").grid(
            row=1, column=2, sticky="w", padx=(
                20, 10), pady=(
                0, 16))
        self.tr_fecha_inicio = DateEntry(form_frame, year=2026)
        self.tr_fecha_inicio.grid(row=1, column=3, sticky="w", pady=(0, 16))

        ttkb.Label(
            form_frame, text="Fecha de terminación").grid(
            row=2, column=0, sticky="w", padx=(
                0, 10), pady=(
                0, 16))
        self.tr_fecha_final = DateEntry(form_frame, year=2026)
        self.tr_fecha_final.grid(row=2, column=1, sticky="w", pady=(0, 16))

        ttkb.Label(
            form_frame,
            text="Descripción").grid(
            row=2,
            column=2,
            sticky="w",
            padx=(
                20,
                10),
            pady=(
                0,
                16))
        self.tr_descripcion = tk.Text(form_frame, height=4, width=40)
        self.tr_descripcion.grid(row=2, column=3, sticky="ew", pady=(0, 16))

        ttkb.Label(
            form_frame, text="Medicamentos").grid(
            row=3, column=0, sticky="w", padx=(
                0, 10), pady=(
                0, 16))
        self.check_medicamentos = {}
        frame_medicamentos = ttkb.Frame(form_frame)
        frame_medicamentos.grid(
            row=3,
            column=1,
            sticky="w",
            pady=(0, 16)
        )

        for id_medicamento, nombre in self.valores_medicamentos:
            var = tk.BooleanVar()
            chk = ttkb.Checkbutton(
                frame_medicamentos,
                text=nombre,
                variable=var
            )
            chk.pack(anchor="w")
            self.check_medicamentos[id_medicamento] = var

    def limpiar(self):
        limpiar_frame(self.frame)

    def ir_lista(self):
        navegar_a_pagina(
            self.frame,
            f"Lista {
                self.tabla}",
            usuario=self.usuario)

    def guardar_valores(self):
        # actualizar los valores del diccionario con los valores de lo widgets
        self.nuevo_registro = {
            'tr_nombre': '',
            'tr_fecha_inicio': "1980-01-01",
            'tr_fecha_final': "1980-01-01",
            'tr_descripcion': '',
            'id_paciente': "",
            'id_doctor': ""
        }

        self.nuevo_registro["tr_nombre"] = self.tr_nombre.get()
        self.nuevo_registro["tr_fecha_inicio"] = self.tr_fecha_inicio.get_date(
        ).strftime("%Y-%m-%d")
        self.nuevo_registro["tr_fecha_final"] = self.tr_fecha_final.get_date(
        ).strftime("%Y-%m-%d")
        self.nuevo_registro["tr_descripcion"] = self.tr_descripcion.get(
            "1.0", "end-1c")
        self.nuevo_registro["id_paciente"] = self.id_paciente.get().split(" ")[
            0]
        self.medicamentos_seleccionados = []

        if self.tipo_usuario == "Administrador": 
            self.nuevo_registro["id_doctor"] = self.id_doctor.get().split(" ")[
                            0]
        else: # si es doctor o enfermera
            self.nuevo_registro["id_doctor"] = self.usuario.get("id_usuarios")

        for id_medicamento, var in self.check_medicamentos.items():
            if var.get():
                self.medicamentos_seleccionados.append(id_medicamento)
        print(
            f"lista de medicamentos seleccionados {
                self.medicamentos_seleccionados}")

    def crear_tratamientos(self):
        if not validar_widget(self.tr_nombre, "Nombre", max_len=50): return
        if not validar_widget(self.tr_descripcion, "Descripción", max_len=100, requerido=False): return
        if not validar_combo(self.id_paciente, "Paciente"): return
        if not validar_combo(self.id_doctor, "Doctor"): return
        self.guardar_valores()
        id_tratamiento = insertar_registro(self.tabla, self.nuevo_registro)
       # medicamentos = obtener_medicinas_de_tratamientos(id_tratamiento)
        # ids_medicamentos = [
        # medicamento["id_medicamentos"]
        # for medicamento in medicamentos
       # ]

        for id_medicamento in self.medicamentos_seleccionados:
            insertar_receta(id_tratamiento, id_medicamento)

        messagebox.showinfo("Crear", "Se creó correctamente el tratamiento")
        navegar_a_pagina(
            self.frame,
            f"Lista {
                self.tabla}",
            usuario=self.usuario)
        # messabox, se creó correctamente.
        # regresar a lista usuarios

    def guardar(self):
        self.crear_tratamientos()
