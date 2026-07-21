#Herencia 
import tkinter as tk
import ttkbootstrap as ttkb

#Clase Padre
class Persona:
    def __init__(self, nombre):
        self.nombre= nombre
    
    def mostrar_nombre(self):
        return self.nombre
    
#Clase hija
class Alumno(Persona):
    def __init__(self, nombre, carrera):
        super().__init__(nombre)
        self.carrera = carrera

#Clase interfaz
class Ventana:
    def __init__(self):
        self.ventana = ttkb.Window(themename="darkly")
        self.ventana.geometry("350x250")
        
        alumno = Alumno("Juan", "DSM") # Crear una instancia de la clase alumno con argumentos
        
        label = ttkb.Label(self.ventana, text=alumno.mostrar_nombre())
        label.pack(pady=50)
        
        self.ventana.mainloop()

#Objeto
objeto = Ventana()
        
        