import tkinter as tk
from tkcalendar import DateEntry

class CrearUsuario:
    def __init__(self, parent):
        self.frame = tk.Frame(parent, bg="#f5f5f5")
        self.frame.pack(fill="both", expand=True)

        self.etiqueta = tk.Label(
            self.frame,
            text="Crear usuario",
            font=("Arial", 14, "bold"),
            bg="#f5f5f5",
            fg="#2c3e50"
        )
        self.etiqueta.pack(pady=20)
        
        tk.Label(self.frame, text="Tipo de usuario").pack(pady=5)
        us_tipo_usuarios = tk.StringVar(value="ninguno")
        tk.Radiobutton(self.frame, text="Administrador", variable=us_tipo_usuarios, value="Administrador").pack()
        tk.Radiobutton(self.frame, text="Doctor", variable=us_tipo_usuarios, value="Doctor").pack()
        tk.Radiobutton(self.frame, text="Enfermera", variable=us_tipo_usuarios, value="Enfermera").pack()
        
       
        tk.Label(self.frame, text="Nombre").pack(pady=5)
        self.us_nombre = tk.Entry(self.frame, width=30)
        self.us_nombre.pack(pady=5)
        
        tk.Label(self.frame, text="Apellidos").pack(pady=5)
        self.us_apellidos = tk.Entry(self.frame, width=30)
        self.us_apellidos.pack(pady=5)
        
        
        tk.Label(self.frame, text="Fecha de nacimiento").pack(pady=5)
        self.us_fecha_nacimiento = DateEntry(self.frame, year= 2026)
        self.us_fecha_nacimiento.pack(pady=5)
        
        tk.Label(self.frame, text="Contraseña").pack(pady=5)
        self.us_contra = tk.Entry(self.frame, width=30)
        self.us_contra.pack(pady=5)
        
        tk.Label(self.frame, text="Teléfono").pack(pady=5)
        self.us_telefono = tk.Entry(self.frame, width=30)
        self.us_telefono.pack(pady=5)
        
        tk.Label(self.frame, text="Correo electrónico").pack(pady=5)
        self.us_correo_electronico = tk.Entry(self.frame, width=30)
        self.us_correo_electronico.pack(pady=5)
        
        tk.Label(self.frame, text="Dirección").pack(pady=5)
        self.us_direccion = tk.Entry(self.frame, width=30)
        self.us_direccion.pack(pady=5)
        
        tk.Label(self.frame, text="Especialidad").pack(pady=5)
        self.us_especialidad = tk.Entry(self.frame, width=30)
        self.us_especialidad.pack(pady=5)
        
        
        
        
        
        
