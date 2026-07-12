import tkinter as tk
import vent

class login():
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Login")
        self.ventana.geometry("300x300")
        
        self.usuario_correcto = "yanet"
        self.password_correcto = 1234
        
        tk.Label(self.ventana, text="Usuario").pack(pady=1, anchor="w")
        entry_usuario = tk.Entry(self.ventana)
        entry_usuario.pack(pady=1, anchor="w")
        
        tk.Label(self.ventana, text="Contraseña").pack(pady=1, anchor="w")
        entry_contra = tk.Entry(self.ventana, show="*")
        entry_contra.pack(pady=1, anchor="w")
        
        tk.Button(self.ventana, text="Cerrar login", command=self.ventana.destroy).pack(pady=5)
        tk.Button(self.ventana, text="Abrir ventana principal", command=vent).pack(pady=5)
      
        self.ventana.mainloop()

    def validar(self):
        usuario = self.usuario_correcto
        contra = self.password_correctowo

objeto = login()
        
        