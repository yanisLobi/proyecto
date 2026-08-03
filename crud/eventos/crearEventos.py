import tkinter as tk
import ttkbootstrap as ttkb
from tkinter import messagebox
from tkcalendar import DateEntry
from tkinter import ttk

from herramients import navegar_a_pagina, validar_widget, validar_combo
from db_mongo import insertar_registro
from db_mysql import obtener_medicinas_de_tratamientos, obtener_valores as obtener_valores_mysql, obtener_ids_tratamientos_visibles

COLORES_EVENTO = {
    "Azul": "#29b6f6",
    "Verde agua": "#26a69a",
    "Morado": "#ab47bc",
    "Naranja rojizo": "#ff7043",
    "Verde": "#66bb6a",
    "Naranja": "#ffa726",
    "Rosa": "#ec407a",
}


class CrearEventosMongo:
    def __init__(self, parent=None, titulo="Crear", usuario=None):
        self.frame = ttkb.Frame(parent)
        self.frame.pack(fill="both", expand=True)
        self.tabla = "consultas"
        self.usuario = usuario or {}

        self.etiqueta = ttkb.Label(
            self.frame,
            text=f"{titulo} recordatorios",
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
            form_frame,
            text="Titulo*").grid(
            row=0,
            column=0,
            sticky="w",
            padx=(
                0,
                10),
            pady=(
                0,
                16))
        self.re_titulo = ttkb.Entry(form_frame, width=30)
        self.re_titulo.grid(row=0, column=1, sticky="ew", pady=(0, 16))

        ttkb.Label(
            form_frame,
            text="Tratamiento*").grid(
            row=0,
            column=2,
            sticky="w",
            padx=(
                20,
                10),
            pady=(
                0,
                16))
        self.tratamientos = self._cargar_tratamientos_combo()
        self.id_tr = tk.StringVar(value="ninguno")
        self.combo_id_tr = ttk.Combobox(
            form_frame,

            textvariable=self.id_tr,
            state="readonly",
            width=27,
            values=self.tratamientos,
        )
        self.combo_id_tr.grid(row=0, column=3, sticky="ew", pady=(0, 16))

        def elemento_seleccionado(event):
            id_tr_seleccionado = self.id_tr.get().strip().split()[0]
            if id_tr_seleccionado != "ninguno":
                # El parámetro 'event' es obligatorio porque .bind() lo envía
                # automáticamente
                meds = obtener_medicinas_de_tratamientos(id_tr_seleccionado)
                self.medicamentos = [
                    f"{m["id_medicamentos"]} {m["me_nombre_comercial"]}" for m in meds]
                if self.re_medicamento:
                    self.re_medicamento.config(state="readonly")
                    self.re_medicamento.config(values=self.medicamentos)
        self.combo_id_tr.bind("<<ComboboxSelected>>", elemento_seleccionado)

        ttkb.Label(
            form_frame,
            text="Estado").grid(
            row=1,
            column=0,
            sticky="w",
            padx=(
                0,
                10),
            pady=(
                0,
                16))
        self.re_estado = ttk.Combobox(
            form_frame,
            values=["Pendiente", "Completado", "Cancelado"],
            state="readonly",
            width=27,
        )
        self.re_estado.set("Pendiente")
        self.re_estado.grid(row=1, column=1, sticky="ew", pady=(0, 16))

        ttkb.Label(
            form_frame,
            text="Fecha").grid(
            row=1,
            column=2,
            sticky="w",
            padx=(
                20,
                10),
            pady=(
                0,
                16))
        self.re_fecha = DateEntry(form_frame)
        self.re_fecha.grid(row=1, column=3, sticky="w", pady=(0, 16))

        ttkb.Label(
            form_frame, text="Hora inicio*").grid(
            row=2, column=0, sticky="w", padx=(
                0, 10), pady=(
                0, 16))
        self.re_hora_inicio = ttkb.Entry(form_frame, width=30)
        self.re_hora_inicio.grid(row=2, column=1, sticky="ew", pady=(0, 16))

        ttkb.Label(
            form_frame,
            text="Hora Fin*").grid(
            row=2,
            column=2,
            sticky="w",
            padx=(
                20,
                10),
            pady=(
                0,
                16))
        self.re_hora_fin = ttkb.Entry(form_frame, width=30)
        self.re_hora_fin.grid(row=2, column=3, sticky="ew", pady=(0, 16))

        ttkb.Label(
            form_frame,
            text="Color").grid(
            row=3,
            column=0,
            sticky="w",
            padx=(
                0,
                10),
            pady=(
                0,
                16))
        self.re_color = tk.StringVar(value=list(COLORES_EVENTO.keys())[0])
        self.combo_color = ttk.Combobox(
            form_frame,
            textvariable=self.re_color,
            state="readonly",
            values=list(COLORES_EVENTO.keys()),
            width=27,
        )
        self.combo_color.grid(row=3, column=1, sticky="ew", pady=(0, 16))

        ttkb.Label(
            form_frame, text="Observaciones").grid(
            row=3, column=2, sticky="nw", padx=(
                20, 10), pady=(
                0, 16))
        self.re_observaciones = tk.Text(form_frame, height=4, width=40)
        self.re_observaciones.grid(row=3, column=3, sticky="ew", pady=(0, 16))

        ttkb.Label(
            form_frame,
            text="Frecuencia").grid(
            row=4,
            column=0,
            sticky="w",
            padx=(
                0,
                10),
            pady=(
                0,
                16))
        self.re_frecuencia = tk.Spinbox(
            form_frame, from_=0, to=96, increment=2, width=30)
        self.re_frecuencia.grid(row=4, column=1, sticky="ew", pady=(0, 16))

        ttkb.Label(
            form_frame, text="Medicamento").grid(
            row=4, column=2, sticky="w", padx=(
                0, 10), pady=(
                0, 16))
        self.re_medicamento = ttk.Combobox(
            form_frame,

            values=["Debes seleccionar un tratamiento"],
            state="disabled",
            width=27,

        )

        self.re_medicamento.grid(row=4, column=3, sticky="ew", pady=(0, 16))

    def limpiar(self):
        limpiar_frame(self.frame)

    def ir_lista(self):
        navegar_a_pagina(self.frame, "Lista eventos", usuario=self.usuario)

    def guardar_valores(self):
        id_tr_seleccionado = self.id_tr.get().strip()
        id_tr_valor = id_tr_seleccionado.split(
        )[0] if id_tr_seleccionado and id_tr_seleccionado != "ninguno" else ""

        self.nuevo_registro = {
            "id_tr": id_tr_valor,
            "re_estado": self.re_estado.get().strip() or "Pendiente",
            "re_observaciones": self.re_observaciones.get(
                "1.0",
                tk.END).strip(),
            "re_titulo": self.re_titulo.get().strip(),
            "re_hora_fin": self.re_hora_fin.get().strip(),
            "re_hora_inicio": self.re_hora_inicio.get().strip(),
            "re_fecha": self.re_fecha.get_date().strftime("%Y-%m-%d"),
            "re_color": COLORES_EVENTO.get(
                self.re_color.get(),
                "#29b6f6"),
            "re_autor": self.usuario.get("id_usuarios"),
            "re_frecuencia": self.re_frecuencia.get(),
            "re_medicamento": self.re_medicamento.get().split()[0]}

    def _cargar_tratamientos_combo(self):
        try:
            todos = obtener_valores_mysql(
                "tratamientos",
                "id_tratamientos",
                "tr_nombre",
                "tr_descripcion",
                solo_activos=True,
            )
            tipo = self.usuario.get("us_tipo_usuario", "")
            ids_visibles = obtener_ids_tratamientos_visibles(
                tipo, self.usuario.get("id_usuarios")
            )
            # None = Administrador ve todos
            if ids_visibles is None:
                return todos
            return [t for t in todos if str(t[0]) in ids_visibles]
        except Exception:
            return []

    def crear_evento(self):
        if not validar_widget(self.re_titulo, "Título", max_len=100): return
        if not validar_combo(self.id_tr, "Tratamiento"): return
        if not validar_widget(self.re_hora_inicio, "Hora inicio", max_len=5): return
        if not validar_widget(self.re_hora_fin, "Hora fin", max_len=5): return
        self.guardar_valores()
        insertar_registro(self.tabla, self.nuevo_registro)
        messagebox.showinfo("Crear", "Se creó correctamente el recordatorio")
        navegar_a_pagina(self.frame, "Lista eventos", usuario=self.usuario)

    def guardar(self):
        self.crear_evento()
