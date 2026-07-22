#Crear una clase que pida un nombre y muestre un saludo

import tkinter as tk
import ttkbootstrap as ttkb

class Formulario():
    def __init__(self):
        self.ventana = ttkb.Window(themename="darkly")
        self.ventana.title("Formulario")
        self.ventana.geometry("350x250")
        
        #Label
        self.label = ttkb.Label(self.ventana, text="Nombre")
        self.label.pack(pady=10)
        
        #Entry
        self.entry = ttkb.Entry(self.ventana)
        self.entry.pack(pady=20)
        
        #Boton
        self.boton = ttkb.Button(self.ventana, text="Mostrar", command=self.mostrar, bootstyle="primary")
        self.boton.pack(pady=10)
        
        #Resultado
        self.resultado = ttkb.Label(self.ventana, text="")
        self.resultado.pack(pady=10)
        
        self.ventana.mainloop()

#Metodos
    def mostrar(self):
        nombre = self.entry.get()
        self.resultado.config(text=f"Hola {nombre}")    

#Objeto
objeto =Formulario()

objeto1 = Formulario()