#Encapsulamiento
#Ocultar atributos para proteger datos

#__atributo

import tkinter as tk

class Usuario:
    def __init__(self):
        self.__nombre=""
        self.ventana = tk.Tk()
        self.ventana.title("Encapsulamiento")
        self.ventana.geometry("300x250")
        
        self.entry = tk.Entry(self.ventana)
        self.entry.pack(pady=20)
        
        self.boton = tk.Button(self.ventana, text="Guardar", command=self.guardar)
        self.boton.pack(pady=20)
        
        self.resultado = tk.Label(self.ventana, text="")
        self.resultado.pack(pady=20)
        
        self.ventana.mainloop()

#Metodos
#setter
    def set_nombre(self,nombre):
        self.__nombre = self.set_nombre
        
#Getter
    def get_nombre(self):
        return self.__nombre
    
    def guardar(self):
        self.set_nombre(self.entry.get())
        self.resultado.config(text=self.get_nombre())

#Objeto
objeto = Usuario()
    