import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta, date
import random

try:
    from db_mongo import obtener_tabla
except Exception:
    obtener_tabla = None

try:
    from db_mysql import obtener_registros as _mysql_get
except Exception:
    _mysql_get = None

_COLORES_EVENTO = ["#26a69a", "#29b6f6", "#ab47bc", "#ff7043", "#66bb6a", "#ffa726", "#ec407a"]
_NOMBRES_DIA = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]


class GoogleCalendarSemanal(ttk.Frame):
    def __init__(self, parent, navegar_cb=None, usuario=None):
        super().__init__(parent)
        self.pack(fill="both", expand=True)
        self.navegar_cb = navegar_cb
        self.usuario = usuario
        self._popup_frame = None
        self.evento_rects = []
        self._eventos_raw = []

        # Parámetros de la interfaz
        self.HORA_INICIO = 8
        self.HORA_FIN = 20
        self.PIXELS_POR_HORA = 60
        self.MARGEN_IZQUIERDO = 70
        self.cabecera_labels = []

        # Semana dinámica: hoy es siempre la columna 0
        self.DIA_ACTUAL_INDEX = 0
        self._actualizar_semana()

        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        # 1. CABECERA FIJA
        self.cabecera = ttk.Frame(self)
        self.cabecera.grid(row=0, column=0, sticky="ew", padx=(self.MARGEN_IZQUIERDO, 20))
        self.configurar_cabecera_dias()

        # 2. CONTENEDOR CON SCROLL
        self.contenedor = ttk.Frame(self)
        self.contenedor.grid(row=1, column=0, sticky="nsew")

        self.canvas = tk.Canvas(self.contenedor, bg="#1e1e1e", highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.contenedor, orient="vertical", command=self.canvas.yview)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        altura_total = (self.HORA_FIN - self.HORA_INICIO + 1) * self.PIXELS_POR_HORA
        self.canvas.configure(scrollregion=(0, 0, 900, altura_total))

        self.canvas.bind("<Configure>", self.al_redimensionar)
        self.canvas.bind("<Button-1>", self._on_canvas_click)

        # Cargar eventos reales desde MongoDB
        self.eventos = self._cargar_eventos_mongo()

    def _actualizar_semana(self):
        """Construye la ventana de 7 días desde hoy y actualiza la hora actual."""
        hoy = date.today()
        self.semana_fechas = [hoy + timedelta(days=i) for i in range(7)]
        self.fecha_a_columna = {
            d.strftime("%Y-%m-%d"): i for i, d in enumerate(self.semana_fechas)
        }
        self.DIAS = [
            f"{_NOMBRES_DIA[d.weekday()]}\n{d.strftime('%d/%m')}"
            for d in self.semana_fechas
        ]
        now = datetime.now()
        self.HORA_ACTUAL = now.hour + now.minute / 60

    def _hora_a_float(self, hora_str):
        try:
            partes = str(hora_str).strip().split(":")
            return int(partes[0]) + int(partes[1]) / 60 if len(partes) >= 2 else int(partes[0])
        except Exception:
            return None

    def _cargar_eventos_mongo(self):
        self._eventos_raw = []
        if obtener_tabla is None:
            print("[Calendario] db_mongo no disponible")
            return []
        try:
            registros = obtener_tabla("consultas")
            print(f"[Calendario] {len(registros)} registros obtenidos de MongoDB")
        except Exception as e:
            print(f"[Calendario] Error al obtener registros: {e}")
            return []

        eventos = []
        for i, reg in enumerate(registros):
            try:
                fecha_val = reg.get("re_fecha", "")
                if hasattr(fecha_val, "strftime"):
                    fecha_str = fecha_val.strftime("%Y-%m-%d")
                else:
                    fecha_str = str(fecha_val).split(" ")[0].split("T")[0]

                col_idx = self.fecha_a_columna.get(fecha_str)
                if col_idx is None:
                    print(f"[Calendario] Evento {i}: fecha '{fecha_str}' fuera de la semana actual")
                    continue

                h_inicio = self._hora_a_float(reg.get("re_hora_inicio", ""))
                h_fin = self._hora_a_float(reg.get("re_hora_fin", ""))
                if h_inicio is None:
                    h_inicio = 9.0
                if h_fin is None or h_fin <= h_inicio:
                    h_fin = h_inicio + 1.0

                titulo = (reg.get("re_titulo") or "Sin título").strip('"').strip()
                color = reg.get("re_color") or random.choice(_COLORES_EVENTO)
                id_evento = reg.get("id", "")
                id_tr = str(reg.get("id_tr", ""))
                eventos.append((titulo, col_idx, h_inicio, h_fin, color, id_evento, id_tr))
                self._eventos_raw.append(reg)
                print(f"[Calendario] Evento añadido: '{titulo}' col={col_idx} {h_inicio}-{h_fin}")
            except Exception as e:
                print(f"[Calendario] Error procesando evento {i}: {e}")
                continue
        return eventos

    def configurar_cabecera_dias(self):
        self.cabecera_labels = []
        for i in range(7):
            self.cabecera.columnconfigure(i, weight=1)
            kwargs = {
                "text": self.DIAS[i],
                "anchor": "center",
                "font": ("Arial", 10, "bold"),
                "justify": "center",
            }
            if i == self.DIA_ACTUAL_INDEX:
                kwargs["foreground"] = "#29b6f6"
            lbl = ttk.Label(self.cabecera, **kwargs)
            lbl.grid(row=0, column=i, pady=10, sticky="ew")
            self.cabecera_labels.append(lbl)

    def actualizar_cabecera(self, ancho_ventana):
        ancho_util = max(ancho_ventana - self.MARGEN_IZQUIERDO - 10, 0)
        ancho_columna = max(int(ancho_util / 7) - 4, 0)
        for lbl in self.cabecera_labels:
            lbl.configure(wraplength=ancho_columna)

    def dibujar_cuadricula(self, ancho_ventana):
        self.canvas.delete("all") 
        ancho_util = ancho_ventana - self.MARGEN_IZQUIERDO - 10
        self.ancho_columna = ancho_util / 7
        
        for hora in range(self.HORA_INICIO, self.HORA_FIN + 1):
            y = (hora - self.HORA_INICIO) * self.PIXELS_POR_HORA
            self.canvas.create_line(self.MARGEN_IZQUIERDO, y, ancho_ventana, y, fill="#2d2d2d", width=1)
            self.canvas.create_text(35, y + 10, text=f"{hora}:00", fill="#888888", font=("Arial", 9))
            
        for i in range(8):
            x = self.MARGEN_IZQUIERDO + (i * self.ancho_columna)
            altura_total = (self.HORA_FIN - self.HORA_INICIO + 1) * self.PIXELS_POR_HORA
            self.canvas.create_line(x, 0, x, altura_total, fill="#2d2d2d", width=1)

    def dibujar_eventos(self):
        self.evento_rects = []
        for idx, (titulo, dia_idx, h_inicio, h_fin, color, id_evento, id_tr) in enumerate(self.eventos):
            x_inicial = self.MARGEN_IZQUIERDO + (dia_idx * self.ancho_columna)
            x_final = x_inicial + self.ancho_columna
            y_inicial = (h_inicio - self.HORA_INICIO) * self.PIXELS_POR_HORA
            y_final = (h_fin - self.HORA_INICIO) * self.PIXELS_POR_HORA
            y_final = max(y_final, y_inicial + 20)  # altura mínima visible

            self.evento_rects.append((x_inicial, y_inicial, x_final, y_final, idx))

            self.canvas.create_rectangle(x_inicial, y_inicial, x_final, y_final, fill=color, outline="", width=0)

            ancho_texto_maximo = int(self.ancho_columna - 15)
            self.canvas.create_text(
                x_inicial + 6, y_inicial + 12,
                text=titulo, anchor="w", fill="white",
                font=("Arial", 9, "bold"), width=ancho_texto_maximo
            )

    def dibujar_indicador_tiempo(self):
        # 1. Calcular la posición Y basada en la hora hardcodeada
        y_linea = (self.HORA_ACTUAL - self.HORA_INICIO) * self.PIXELS_POR_HORA
        
        # 2. Calcular los límites X para que solo cubra la columna del día actual
        x_inicial = self.MARGEN_IZQUIERDO + (self.DIA_ACTUAL_INDEX * self.ancho_columna)
        x_final = x_inicial + self.ancho_columna
        
        # Color rojo característico de Google Calendar
        color_indicador = "#ea4335" 
        
        # 3. Dibujar la línea horizontal en la columna correcta
        self.canvas.create_line(x_inicial, y_linea, x_final, y_linea, fill=color_indicador, width=2)
        
        # 4. Dibujar el círculo indicador en el extremo izquierdo de la columna
        radio_circulo = 5
        self.canvas.create_oval(
            x_inicial - radio_circulo, y_linea - radio_circulo,
            x_inicial + radio_circulo, y_linea + radio_circulo,
            fill=color_indicador, outline=""
        )

    def al_redimensionar(self, event):
        now = datetime.now()
        self.HORA_ACTUAL = now.hour + now.minute / 60
        self.dibujar_cuadricula(event.width)
        self.dibujar_eventos()
        self.dibujar_indicador_tiempo()
        self.actualizar_cabecera(event.width)

    # ── CLICK EN EL CANVAS ──────────────────────────────────────────────

    def _on_canvas_click(self, event):
        cx = self.canvas.canvasx(event.x)
        cy = self.canvas.canvasy(event.y)
        for x1, y1, x2, y2, idx in self.evento_rects:
            if x1 <= cx <= x2 and y1 <= cy <= y2:
                self._abrir_popup(idx)
                return
        self._cerrar_popup()

    # ── POPUP ────────────────────────────────────────────────────────────

    def _cerrar_popup(self):
        if self._popup_frame is not None:
            self._popup_frame.destroy()
            self._popup_frame = None

    def _navegar(self, tipo, nombre_clase, **kwargs):
        self._cerrar_popup()
        if self.navegar_cb:
            self.navegar_cb(tipo, nombre_clase, **kwargs)

    def _campo(self, parent, etiqueta, valor, bg):
        fila = tk.Frame(parent, bg=bg)
        fila.pack(fill="x", padx=10, pady=1)
        tk.Label(fila, text=f"{etiqueta}:", fg="#aaaaaa", bg=bg,
                 font=("Arial", 8), anchor="w", width=12).pack(side="left")
        tk.Label(fila, text=str(valor) if valor else "—", fg="#e0e0e0", bg=bg,
                 font=("Arial", 8), anchor="w", wraplength=155, justify="left").pack(side="left", fill="x", expand=True)

    def _seccion(self, parent, titulo_sec, campos, bg_header, bg_body, link_cmd=None):
        header = tk.Frame(parent, bg=bg_header)
        header.pack(fill="x", pady=(8, 0))
        tk.Label(header, text=titulo_sec, fg="white", bg=bg_header,
                 font=("Arial", 9, "bold"), padx=10, pady=4).pack(side="left")
        if link_cmd and self.navegar_cb:
            btn = tk.Label(header, text="Editar →", fg="#29b6f6", bg=bg_header,
                           font=("Arial", 8, "underline"), cursor="hand2", padx=8)
            btn.pack(side="right")
            btn.bind("<Button-1>", lambda e, fn=link_cmd: fn())
        body = tk.Frame(parent, bg=bg_body)
        body.pack(fill="x")
        for etiqueta, valor in campos:
            self._campo(body, etiqueta, valor, bg_body)

    def _abrir_popup(self, idx):
        self._cerrar_popup()

        raw = self._eventos_raw[idx]
        titulo, col_idx, h_inicio, h_fin, color, id_evento, id_tr = self.eventos[idx]

        # ── Cargar datos relacionados desde MySQL ──
        trat, pac, doc, enf = {}, {}, {}, {}
        id_trat, id_paciente, id_doctor, id_enfermera = None, None, None, None
        if _mysql_get and id_tr:
            try:
                trat_list = _mysql_get("tratamientos", "id_tratamientos", id_tr)
                trat = trat_list[0] if trat_list else {}
                id_trat = trat.get("id_tratamientos")
                id_paciente = trat.get("id_paciente")
                id_doctor = trat.get("id_doctor")
            except Exception as e:
                print(f"[Popup] Error tratamiento: {e}")
            if id_paciente:
                try:
                    pac_list = _mysql_get("pacientes", "id_pacientes", id_paciente)
                    pac = pac_list[0] if pac_list else {}
                    id_enfermera = pac.get("id_enfermera_principal")
                except Exception as e:
                    print(f"[Popup] Error paciente: {e}")
            if id_doctor:
                try:
                    doc_list = _mysql_get("usuarios", "id_usuarios", id_doctor)
                    doc = doc_list[0] if doc_list else {}
                except Exception as e:
                    print(f"[Popup] Error doctor: {e}")
            if id_enfermera:
                try:
                    enf_list = _mysql_get("usuarios", "id_usuarios", id_enfermera)
                    enf = enf_list[0] if enf_list else {}
                except Exception as e:
                    print(f"[Popup] Error enfermera: {e}")

        # ── Construir el frame del popup ──
        BG       = "#1e1e2e"
        BG_HDR   = "#2a2a3e"
        BG_BODY  = "#252535"

        popup = tk.Frame(self, bg=BG, bd=1, relief="solid")
        popup.place(relx=1.0, rely=0.04, anchor="ne", x=-20, relheight=0.90, width=290)
        self._popup_frame = popup

        # Barra de título
        title_bar = tk.Frame(popup, bg="#161625")
        title_bar.pack(fill="x")
        tk.Label(title_bar, text="Detalle del evento", fg="white", bg="#161625",
                 font=("Arial", 10, "bold"), padx=10, pady=7).pack(side="left")
        close_lbl = tk.Label(title_bar, text="✕", fg="#aaaaaa", bg="#161625",
                              font=("Arial", 11), padx=10, cursor="hand2")
        close_lbl.pack(side="right")
        close_lbl.bind("<Button-1>", lambda e: self._cerrar_popup())

        # Área scrollable interna
        sc_canvas = tk.Canvas(popup, bg=BG, highlightthickness=0)
        sc_scroll = ttk.Scrollbar(popup, orient="vertical", command=sc_canvas.yview)
        sc_canvas.configure(yscrollcommand=sc_scroll.set)
        sc_scroll.pack(side="right", fill="y")
        sc_canvas.pack(side="left", fill="both", expand=True)
        inner = tk.Frame(sc_canvas, bg=BG)
        win_id = sc_canvas.create_window((0, 0), window=inner, anchor="nw")
        inner.bind("<Configure>", lambda e: sc_canvas.configure(scrollregion=sc_canvas.bbox("all")))
        sc_canvas.bind("<Configure>", lambda e, wid=win_id: sc_canvas.itemconfig(wid, width=e.width))

        # ── Sección Evento ──
        self._seccion(inner, "Evento", [
            ("Título",        titulo),
            ("Fecha",         raw.get("re_fecha", "—")),
            ("Inicio",        raw.get("re_hora_inicio", "—")),
            ("Fin",           raw.get("re_hora_fin", "—")),
            ("Estado",        raw.get("re_estado", "—")),
            ("Observaciones", raw.get("re_observaciones", "—")),
        ], BG_HDR, BG_BODY,
        link_cmd=lambda iv=id_evento: self._navegar("mongo", "Actualizar eventos", id_seleccionado=iv))

        # ── Sección Tratamiento ──
        self._seccion(inner, "Tratamiento", [
            ("Nombre",      trat.get("tr_nombre", "—")),
            ("Inicio",      trat.get("tr_fecha_inicio", "—")),
            ("Fin",         trat.get("tr_fecha_final", "—")),
            ("Descripción", trat.get("tr_descripcion", "—")),
        ], BG_HDR, BG_BODY,
        link_cmd=lambda it=id_trat: self._navegar("mysql", "Actualizar tratamientos", id_seleccionado=it) if it else None)

        # ── Sección Paciente ──
        self._seccion(inner, "Paciente", [
            ("Nombre",    f"{pac.get('pa_nombre', '')} {pac.get('pa_apellidos', '')}".strip() or "—"),
            ("Nacimiento", pac.get("pa_fecha_nacimiento", "—")),
            ("Contacto",  pac.get("pa_nombre_contacto_emergencia", "—")),
            ("Tel. emergencia", pac.get("pa_tel_contacto_emergencia", "—")),
        ], BG_HDR, BG_BODY,
        link_cmd=lambda ip=id_paciente: self._navegar("mysql", "Actualizar pacientes", id_seleccionado=ip) if ip else None)

        # ── Sección Doctor ──
        self._seccion(inner, "Doctor", [
            ("Nombre",      f"{doc.get('us_nombre', '')} {doc.get('us_apellidos', '')}".strip() or "—"),
            ("Especialidad", doc.get("us_especialidad", "—")),
        ], BG_HDR, BG_BODY,
        link_cmd=lambda id_d=id_doctor: self._navegar("mysql", "Actualizar usuarios", id_seleccionado=id_d) if id_d else None)

        # ── Sección Enfermera ──
        self._seccion(inner, "Enfermera", [
            ("Nombre", f"{enf.get('us_nombre', '')} {enf.get('us_apellidos', '')}".strip() or "—"),
        ], BG_HDR, BG_BODY,
        link_cmd=lambda id_e=id_enfermera: self._navegar("mysql", "Actualizar usuarios", id_seleccionado=id_e) if id_e else None)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("AbueCare - Agenda Semanal")
    root.geometry("900x600")
    GoogleCalendarSemanal(root)
    root.mainloop()