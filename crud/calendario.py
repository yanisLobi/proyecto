import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta, date
import random

from herramients import regresar_string

try:
    from db_mongo import obtener_tabla, actualizar_registro as _mongo_actualizar
except Exception:
    obtener_tabla = None
    _mongo_actualizar = None

try:
    from db_mysql import obtener_registros as _mysql_get, obtener_medicinas_de_tratamientos as _mysql_medicinas_tratamiento, obtener_ids_tratamientos_visibles as _mysql_ids_visibles
except Exception:
    _mysql_get = None
    _mysql_medicinas_tratamiento = None
    _mysql_ids_visibles = None

_COLORES_EVENTO = ["#26a69a", "#29b6f6", "#ab47bc", "#ff7043", "#66bb6a", "#ffa726", "#ec407a"]
_NOMBRES_DIA = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]


def _mezclar_color(hex_color, bg="#1e1e1e", factor=0.45):
    """Mezcla hex_color con bg al factor dado (0=todo bg, 1=color original)."""
    try:
        r1, g1, b1 = int(hex_color[1:3], 16), int(hex_color[3:5], 16), int(hex_color[5:7], 16)
        r2, g2, b2 = int(bg[1:3], 16), int(bg[3:5], 16), int(bg[5:7], 16)
        r = int(r1 * factor + r2 * (1 - factor))
        g = int(g1 * factor + g2 * (1 - factor))
        b = int(b1 * factor + b2 * (1 - factor))
        return f"#{r:02x}{g:02x}{b:02x}"
    except Exception:
        return hex_color


class CalendarioRecordatorios(ttk.Frame):
    def __init__(self, parent, navegar_cb=None, usuario=None):
        super().__init__(parent)
        self.pack(fill="both", expand=True)
        self.navegar_cb = navegar_cb
        self.usuario = usuario
        self._popup_frame = None
        self.evento_rects = []
        self._eventos_raw = []

        # Parámetros de la interfaz
        self.HORA_INICIO = 0
        self.HORA_FIN = 24
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
            return int(partes[0]) + (int(partes[1]) / 60 if len(partes) >= 2 else int(partes[0]))
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

        tipo_usu = (self.usuario or {}).get("us_tipo_usuario")
        id_usu = (self.usuario or {}).get("id_usuarios")
        ids_permitidos = None
        if _mysql_ids_visibles and tipo_usu:
            try:
                ids_permitidos = _mysql_ids_visibles(tipo_usu, id_usu)
            except Exception as e:
                print(f"[Calendario] Error al obtener ids permitidos: {e}")

        eventos = []
        for i, reg in enumerate(registros):
            try:
                # filtrar por tratamientos visibles
                if ids_permitidos is not None and str(reg.get("id_tr", "")) not in ids_permitidos:
                    continue

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
                # Buscar nombre del paciente vía tratamiento
                nombre_paciente = ""
                if _mysql_get and id_tr:
                    try:
                        trat_l = _mysql_get("tratamientos", "id_tratamientos", id_tr, False)
                        if trat_l:
                            id_pac = trat_l[0].get("id_paciente")
                            if id_pac:
                                pac_l = _mysql_get("pacientes", "id_pacientes", id_pac, False)
                                if pac_l:
                                    p = pac_l[0]
                                    nombre_paciente = f"{p.get('pa_nombre', '')} {p.get('pa_apellidos', '')}".strip()
                    except Exception:
                        pass
                eventos.append((titulo, col_idx, h_inicio, h_fin, color, id_evento, id_tr, nombre_paciente))
                self._eventos_raw.append(reg)
                #print(f"[Calendario] Evento añadido: '{titulo}' col={col_idx} {h_inicio}-{h_fin}")
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
        for idx, (titulo, dia_idx, h_inicio, h_fin, color, id_evento, id_tr, nombre_paciente) in enumerate(self.eventos):
            x_inicial = self.MARGEN_IZQUIERDO + (dia_idx * self.ancho_columna)
            x_final = x_inicial + self.ancho_columna
            y_inicial = (h_inicio - self.HORA_INICIO) * self.PIXELS_POR_HORA
            y_final = (h_fin - self.HORA_INICIO) * self.PIXELS_POR_HORA
            y_final = max(y_final, y_inicial + 30)  # altura mínima para dos líneas

            self.evento_rects.append((x_inicial, y_inicial, x_final, y_final, idx))

            completado = self._eventos_raw[idx].get("re_estado", "") == "Completado"
            color_rect = _mezclar_color(color) if completado else color
            texto_fill = "#888888" if completado else "white"
            sub_fill   = "#555555" if completado else "#d0d0d0"

            self.canvas.create_rectangle(x_inicial, y_inicial, x_final, y_final, fill=color_rect, outline="", width=0)

            ancho_texto_maximo = int(self.ancho_columna - 10)
            self.canvas.create_text(
                x_inicial + 5, y_inicial + 10,
                text=titulo, anchor="w", fill=texto_fill,
                font=("Arial", 9, "bold"), width=ancho_texto_maximo
            )
            if nombre_paciente:
                self.canvas.create_text(
                    x_inicial + 5, y_inicial + 22,
                    text=nombre_paciente, anchor="w", fill=sub_fill,
                    font=("Arial", 8), width=ancho_texto_maximo
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

    def _normalizar_valor(self, valor):
        if valor is None:
            return "—"
        if isinstance(valor, bool):
            return "Sí" if valor else "No"
        if isinstance(valor, (list, tuple, dict)):
            return str(valor)
        return str(valor)

    def _identificador_registro(self, datos):
        if not isinstance(datos, dict):
            return None

        id_val = None
        for clave in ("id", "id_tratamientos", "id_pacientes", "id_usuarios", "id_medicamentos", "id_paciente", "id_doctor", "id_enfermera_principal"):
            if clave in datos and datos[clave] not in (None, "", 0):
                id_val = datos[clave]
                break

        nombre = None
        apellido = None

        for clave in ("tr_nombre", "pa_nombre", "us_nombre", "me_nombre_comercial"):
            if clave in datos and datos[clave] not in (None, ""):
                nombre = datos[clave]
                break

        for clave in ("pa_apellidos", "us_apellidos", "me_nombre_tecnico"):
            if clave in datos and datos[clave] not in (None, ""):
                apellido = datos[clave]
                break

        partes = []
        if id_val is not None:
            partes.append(str(id_val))
        if nombre:
            partes.append(str(nombre))
        if apellido:
            partes.append(str(apellido))

        return " ".join(partes).strip() or None

    def _filtrar_campos(self, datos, incluir_identificador=False):
        if not isinstance(datos, dict):
            return []
        campos = []

        if incluir_identificador:
            resumen = self._identificador_registro(datos)
            if resumen:
                campos.append(("Identificación", resumen))

        for nombre, valor in datos.items():
            clave = str(nombre).strip()
            if not clave:
                continue
            clave_lower = clave.lower()
            if clave_lower in {"id", "_id"} or clave_lower.startswith("id_") or clave_lower.endswith("_id"):
                continue
            if clave_lower.endswith("_activo") or "_activo" in clave_lower:
                continue
            if "contrase" in clave_lower or "password" in clave_lower or "passwd" in clave_lower:
                continue
            campos.append((regresar_string(clave), self._normalizar_valor(valor)))
        return campos

    def _campo(self, parent, etiqueta, valor, bg):
        fila = tk.Frame(parent, bg=bg)
        fila.pack(fill="x", padx=10, pady=1)
        tk.Label(fila, text=f"{etiqueta}:", fg="#aaaaaa", bg=bg,
                 font=("Arial", 8), anchor="w", width=18).pack(side="left")
        tk.Label(fila, text=str(valor) if valor not in (None, "", "—") else "—", fg="#e0e0e0", bg=bg,
                 font=("Arial", 8), anchor="w", wraplength=360, justify="left").pack(side="left", fill="x", expand=True)

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
        titulo, col_idx, h_inicio, h_fin, color, id_evento, id_tr, nombre_paciente = self.eventos[idx]

        # ── Cargar datos relacionados desde MySQL ──
        trat, pac, doc, enf = {}, {}, {}, {}
        medicinas = []
        id_trat, id_paciente, id_doctor, id_enfermera = None, None, None, None
        if _mysql_get and id_tr:
            try:
                trat_list = _mysql_get("tratamientos", "id_tratamientos", id_tr, False)
                trat = trat_list[0] if trat_list else {}
                id_trat = trat.get("id_tratamientos")
                id_paciente = trat.get("id_paciente")
                id_doctor = trat.get("id_doctor")
            except Exception as e:
                print(f"[Popup] Error tratamiento: {e}")
            if id_paciente:
                try:
                    pac_list = _mysql_get("pacientes", "id_pacientes", id_paciente, False)
                    pac = pac_list[0] if pac_list else {}
                    id_enfermera = pac.get("id_enfermera_principal")
                except Exception as e:
                    print(f"[Popup] Error paciente: {e}")
            if id_doctor:
                try:
                    doc_list = _mysql_get("usuarios", "id_usuarios", id_doctor, False)
                    doc = doc_list[0] if doc_list else {}
                except Exception as e:
                    print(f"[Popup] Error doctor: {e}")
            if id_enfermera:
                try:
                    enf_list = _mysql_get("usuarios", "id_usuarios", id_enfermera, False)
                    enf = enf_list[0] if enf_list else {}
                except Exception as e:
                    print(f"[Popup] Error enfermera: {e}")
            if id_trat and _mysql_medicinas_tratamiento:
                try:
                    medicinas = _mysql_medicinas_tratamiento(id_trat) or []
                except Exception as e:
                    print(f"[Popup] Error medicinas: {e}")

        # ── Construir el frame del popup ──
        BG       = "#1e1e2e"
        BG_HDR   = "#2a2a3e"
        BG_BODY  = "#252535"

        popup = tk.Frame(self, bg=BG, bd=1, relief="solid")
        popup.place(relx=1.0, rely=0.04, anchor="ne", x=-20, relheight=0.90, width=620)
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

        # Botón “Marcar como completado” (solo si no está ya completado)
        if raw.get("re_estado", "") != "Completado" and _mongo_actualizar:
            def _marcar_completado(iv=id_evento, _idx=idx):
                try:
                    _mongo_actualizar("consultas", {"re_estado": "Completado"}, "id", iv)
                    self._eventos_raw[_idx]["re_estado"] = "Completado"
                except Exception as ex:
                    print(f"[Popup] Error al marcar completado: {ex}")
                    return
                self._cerrar_popup()
                self.eventos = self._cargar_eventos_mongo()
                ancho = self.canvas.winfo_width()
                if ancho > 1:
                    self.dibujar_cuadricula(ancho)
                    self.dibujar_eventos()
                    self.dibujar_indicador_tiempo()
            btn_completar = tk.Button(
                popup, text="✓ Marcar como completado",
                bg="#2e7d32", fg="white", relief="flat",
                font=("Arial", 9, "bold"), cursor="hand2",
                activebackground="#1b5e20", activeforeground="white",
                command=_marcar_completado, pady=6,
            )
            btn_completar.pack(fill="x", padx=0)

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

        tipo_usu = (self.usuario or {}).get("us_tipo_usuario", "")
        puede_editar_usuarios    = tipo_usu == "Administrador"
        puede_editar_resto       = tipo_usu in ("Administrador", "Doctor")

        # ── Sección Evento ──
        self._seccion(inner, "Evento", [
            ("Título", titulo),
            ("Fecha", raw.get("re_fecha", "—")),
            ("Inicio", raw.get("re_hora_inicio", "—")),
            ("Fin", raw.get("re_hora_fin", "—")),
            ("Estado", raw.get("re_estado", "—")),
            ("Observaciones", raw.get("re_observaciones", "—")),
        ], BG_HDR, BG_BODY,
        link_cmd=(lambda iv=id_evento: self._navegar("mongo", "Actualizar eventos", id_seleccionado=iv)) if puede_editar_resto else None)

        # ── Sección Tratamiento ──
        if trat:
            self._seccion(inner, "Tratamiento", self._filtrar_campos(trat, incluir_identificador=True), BG_HDR, BG_BODY,
                         link_cmd=(lambda it=id_trat: self._navegar("mysql", "Actualizar tratamientos", id_seleccionado=it) if it else None) if puede_editar_resto else None)
        else:
            self._seccion(inner, "Tratamiento", [("Detalle", "Sin tratamiento asociado")], BG_HDR, BG_BODY)

        # ── Sección Paciente ──
        if pac:
            self._seccion(inner, "Paciente", self._filtrar_campos(pac, incluir_identificador=True), BG_HDR, BG_BODY,
                         link_cmd=(lambda ip=id_paciente: self._navegar("mysql", "Actualizar pacientes", id_seleccionado=ip) if ip else None) if puede_editar_resto else None)
        else:
            self._seccion(inner, "Paciente", [("Detalle", "Sin paciente asociado")], BG_HDR, BG_BODY)

        # ── Sección Doctor ──
        if doc:
            self._seccion(inner, "Doctor", self._filtrar_campos(doc, incluir_identificador=True), BG_HDR, BG_BODY,
                         link_cmd=(lambda id_d=id_doctor: self._navegar("mysql", "Actualizar usuarios", id_seleccionado=id_d) if id_d else None) if puede_editar_usuarios else None)
        else:
            self._seccion(inner, "Doctor", [("Detalle", "Sin doctor asociado")], BG_HDR, BG_BODY)

        # ── Sección Enfermera ──
        if enf:
            self._seccion(inner, "Enfermera", self._filtrar_campos(enf, incluir_identificador=True), BG_HDR, BG_BODY,
                         link_cmd=(lambda id_e=id_enfermera: self._navegar("mysql", "Actualizar usuarios", id_seleccionado=id_e) if id_e else None) if puede_editar_usuarios else None)
        else:
            self._seccion(inner, "Enfermera", [("Detalle", "Sin enfermera asociada")], BG_HDR, BG_BODY)

        # ── Sección Medicinas ──
        if medicinas:
            for i, med in enumerate(medicinas, start=1):
                id_med = med.get("id_medicamentos")
                self._seccion(inner, f"Medicina {i}", self._filtrar_campos(med, incluir_identificador=True), BG_HDR, BG_BODY,
                             link_cmd=(lambda im=id_med: self._navegar("mysql", "Actualizar medicamentos", id_seleccionado=im) if im else None) if puede_editar_resto else None)
        else:
            self._seccion(inner, "Medicinas", [("Detalle", "Sin medicinas asociadas al tratamiento")], BG_HDR, BG_BODY)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("AbueCare - Agenda Semanal")
    root.geometry("900x600")
    CalendarioRecordatorios(root)
    root.mainloop()
    