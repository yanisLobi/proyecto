#Crear una ventana, usar etiqueta, boton y que al darle clic cambie el texto.

import tkinter as tk

class Aplicacion:
    #Constructor
    def __init__(self):
        #Ventana
        self.ventana = tk.Tk()
        self.ventana.title("POO")
        self.ventana.geometry("300x200")
        
        #Label
        self.label = tk.Label(self.ventana, text="Texto original")
        self.label.pack(pady=20)
        
        #Boton
        self.boton = tk.Button(self.ventana, text="Cambiar", command=self.cambiar_texto)
        self.boton.pack()
        
        #Ejecucion
        self.ventana.mainloop()
    
    #Metodos
    def cambiar_texto(self):
        self.label.config(text="Texto modificado")
    
#crear objeto
objeto = Aplicacion()
        