import tkinter as tk


from conexion import conectar
from herramientas import navegar_a_pagina
from tkinter import messagebox
from tkcalendar import DateEntry


class CrearPacientes:
    def __init__(self, parent):
        self.frame = tk.Frame(parent, bg="#f5f5f5")
        self.frame.pack(fill="both", expand=True)
    
        self.etiqueta = tk.Label(
            self.frame,
            text="Crear pacientes",
            font=("Arial", 14, "bold"),
            bg="#f5f5f5",
            fg="#2c3e50"
        )
        self.etiqueta.pack(pady=20)


        tk.Label(self.frame, text="Nombre").pack(pady=5)
        self.nombre = tk.Entry(self.frame, width=30)
        self.nombre.pack(pady=5)
        
        tk.Label(self.frame, text="Apellidos").pack(pady=5)
        self.apellidos = tk.Entry(self.frame, width=30)
        self.apellidos.pack(pady=5)
        
        tk.Label(self.frame, text="Edad").pack(pady=5)
        self.edad = tk.Spinbox(self.frame, from_=50, to=90)
        self.edad.pack(pady=5)
        
        tk.Label(self.frame, text="Sexo").pack(pady=5)
        self.radio_sexo = tk.StringVar(value="ninguno")
        tk.Radiobutton(self.frame, text="Masculino", 
                       variable=self.radio_sexo, value="Masculino")
        tk.Radiobutton(self.frame, text="Femenino",
                          variable=self.radio_sexo, value="Femenino")
        #falta cambiar todo
        tk.Label(self.frame, text="Fecha de nacimiento").pack(pady=5)
        self.edad = tk.Spinbox(self.frame, from_=50, to=90)
        self.edad.pack(pady=5)
        
        tk.Label(self.frame, text="Nombre del contacto de emergencia").pack(pady=5)
        self.nombre_contacto = tk.Entry(self.frame, width=30)
        self.nombre_contacto.pack(pady=5)
        
        tk.Label(self.frame, text="Telefono de Contacto de emergencia").pack(pady=5)
        self.tel_contacto = tk.Spinbox(self.frame, from_=50, to=90)
        self.tel_contacto.pack(pady=5)
        
        self.fecha = DateEntry(self.frame, year=1960)
        self.fecha.pack(pady=5)
        
        
       
        tk.Button(self.frame, text="Guardar Paciente", command=self.guardar).pack(pady=10)
        tk.Button(self.frame, text="Cancelar", command=self.cancelar).pack(pady=10)
        tk.Button(self.frame, text="Limpiar", command=self.limpiar).pack(pady=10)
        
        self.conexion = conectar()
    
    def validar_campos(self):
    #verificar que ninguno de los campos del formulario este vacip
        if (
        self.nombre.get().strip() == "" or
        self.apellidos.get().strip() == "" or
        self.edad.get().strip() == "" or
        self.radio_sexo.get().strip() == ""
        ):
            return False

        return True
        
    def guardar(self):
        
        if (not self.validar_campos):
            messagebox.showwarning("Campos vacíos", "Todos los campos son obligatorios")
            return
        
        nombre = self.nombre.get().strip()
        apellido= self.apellidos.get().strip()
        edad= self.edad.get().strip()
        sexo= self.radio_sexo.get().strip()
        
        # Abre la conexión
        cursor = self.conexion.cursor()
        sql = "INSERT INTO `pacientes` (`id_pa`, `pa_nombre`, `pa_apellidos`, `pa_fecha_nacimiento`, `pa_nombre_contacto_emergencia`, `pa_tel_contacto_emergencia`) VALUES (NULL,%s, %s, %s, %s,%s,%s)"
        cursor.execute(sql, (nombre, apellido, edad, sexo))
        self.conexion.commit()
        cursor.close()
        self.conexion.close()
        
        messagebox.showinfo("Saludo", "¡Hola! Has creado un nuevo paciente")
        navegar_a_pagina(self.frame,"Lista pacientes")
            
        
    def cancelar(self):
        navegar_a_pagina(self.frame, "Lista pacientes")
    
    def limpiar():
        #Aqui vamos a tener que limpiar todos los campos
        pass
        
    

def main():
    root = tk.Tk()
    root.title("Crear Pacientes")
    root.geometry("500x400")
    CrearPacientes(root)
    root.mainloop()
    
if __name__ == "__main__":
    main()
       