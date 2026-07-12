#Herencia 
import tkinter as tk

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
        self.ventana = tk.Tk()
        self.ventana.geometry("350x250")
        
        alumno = Alumno("Juan", "DSM") # Crear una instancia de la clase alumno con argumentos
        
        label = tk.Label(self.ventana, text=alumno.mostrar_nombre())
        label.pack(pady=50)
        
        self.ventana.mainloop()

#Objeto
objeto = Ventana()
        
        