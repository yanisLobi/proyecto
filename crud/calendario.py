import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttkb

class GoogleCalendarSemanal(ttkb.Window):
    def __init__(self):
        super().__init__(themename="darkly")
        self.title("AbueCare - Agenda Semanal")
        self.geometry("900x600")
        
        # Parámetros de la interfaz
        self.HORA_INICIO = 8       
        self.HORA_FIN = 20         
        self.PIXELS_POR_HORA = 60  
        self.MARGEN_IZQUIERDO = 70 
        self.DIAS = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        
        # --- DATOS HARDCODEADOS DEL TIEMPO ACTUAL ---
        self.DIA_ACTUAL_INDEX = 2  # 2 = Miércoles (0=Lunes, 1=Martes...)
        self.HORA_ACTUAL = 13.5     # 13.5 = 1:30 PM (Representación decimal de la hora)
        # --------------------------------------------

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
        
        self.eventos = [
            ("Llamada Familiar", 0, 9.0, 10.5, "#26a69a"),   
            ("Chequeo Médico", 2, 11.0, 13.0, "#29b6f6"),   
            ("Terapia Física", 4, 15.5, 17.0, "#ab47bc"),   
            ("Llamada Soporte", 6, 10.0, 11.5, "#ff7043"),  
        ]

    def configurar_cabecera_dias(self):
        for i in range(7):
            self.cabecera.columnconfigure(i, weight=1)
            # Resaltamos visualmente el texto del día actual si coincide
            color_texto = "#29b6f6" if i == self.DIA_ACTUAL_INDEX else "white"
            lbl = ttk.Label(self.cabecera, text=self.DIAS[i], anchor="center", 
                            font=("Arial", 10, "bold"), foreground=color_texto)
            lbl.grid(row=0, column=i, pady=10, sticky="ew")

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
        self.dibujar_cuadricula(event.width)
        self.dibujar_eventos()
        self.dibujar_indicador_tiempo() # Lo llamamos al final para que quede por encima de las líneas y eventos

if __name__ == "__main__":
    app = GoogleCalendarSemanal()
    app.mainloop()