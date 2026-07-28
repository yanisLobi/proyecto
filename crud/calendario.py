import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta, date
import random

try:
    from db_mongo import obtener_tabla
except Exception:
    obtener_tabla = None

_COLORES_EVENTO = ["#26a69a", "#29b6f6", "#ab47bc", "#ff7043", "#66bb6a", "#ffa726", "#ec407a"]
_NOMBRES_DIA = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]


class GoogleCalendarSemanal(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill="both", expand=True)

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
        if obtener_tabla is None:
            return []
        try:
            registros = obtener_tabla("consultas")
        except Exception:
            return []

        eventos = []
        for i, reg in enumerate(registros):
            try:
                # re_fecha puede llegar como str, datetime o date
                fecha_val = reg.get("re_fecha", "")
                if hasattr(fecha_val, "strftime"):
                    fecha_str = fecha_val.strftime("%Y-%m-%d")
                else:
                    fecha_str = str(fecha_val).split(" ")[0].split("T")[0]

                col_idx = self.fecha_a_columna.get(fecha_str)
                if col_idx is None:
                    continue

                h_inicio = self._hora_a_float(reg.get("re_hora_inicio", ""))
                h_fin = self._hora_a_float(reg.get("re_hora_fin", ""))
                if h_inicio is None:
                    h_inicio = 9.0
                if h_fin is None or h_fin <= h_inicio:
                    h_fin = h_inicio + 1.0

                titulo = reg.get("re_titulo") or "Sin título"
                color = reg.get("re_color") or random.choice(_COLORES_EVENTO)
                eventos.append((titulo, col_idx, h_inicio, h_fin, color))
            except Exception:
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
        for titulo, dia_idx, h_inicio, h_fin, color in self.eventos:
            x_inicial = self.MARGEN_IZQUIERDO + (dia_idx * self.ancho_columna) + 4
            x_final = x_inicial + self.ancho_columna - 8
            y_inicial = (h_inicio - self.HORA_INICIO) * self.PIXELS_POR_HORA + 2
            y_final = (h_fin - self.HORA_INICIO) * self.PIXELS_POR_HORA - 2
            
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

if __name__ == "__main__":
    root = tk.Tk()
    root.title("AbueCare - Agenda Semanal")
    root.geometry("900x600")
    GoogleCalendarSemanal(root)
    root.mainloop()