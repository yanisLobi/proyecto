#Crear una ventana, usar etiqueta, boton y que al darle clic cambie el texto.

import tkinter as tk
import ttkbootstrap as ttkb

class Aplicacion:
    #Constructor
    def __init__(self):
        #Ventana
        self.ventana = ttkb.Window(themename="darkly")
        self.ventana.title("POO")
        self.ventana.geometry("300x200")
        
        #Label
        self.label = ttkb.Label(self.ventana, text="Texto original")
        self.label.pack(pady=20)
        
        #Boton
        self.boton = ttkb.Button(self.ventana, text="Cambiar", command=self.cambiar_texto, bootstyle="primary")
        self.boton.pack()
        
        #Ejecucion
        self.ventana.mainloop()
    
    #Metodos
    def cambiar_texto(self):
        self.label.config(text="Texto modificado")
   
#crear objeto
objeto = Aplicacion()
        