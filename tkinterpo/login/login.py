import tkinter as tk
import ttkbootstrap as ttkb
import vent

class login():
    def __init__(self):
        self.ventana = ttkb.Window(themename="darkly")
        self.ventana.title("Login")
        self.ventana.geometry("300x300")
        
        self.usuario_correcto = "yanet"
        self.password_correcto = 1234
        
        ttkb.Label(self.ventana, text="Usuario").pack(pady=1, anchor="w")
        entry_usuario = ttkb.Entry(self.ventana)
        entry_usuario.pack(pady=1, anchor="w")
        
        ttkb.Label(self.ventana, text="Contraseña").pack(pady=1, anchor="w")
        entry_contra = ttkb.Entry(self.ventana, show="*")
        entry_contra.pack(pady=1, anchor="w")
        
        ttkb.Button(
            self.ventana,
            text="Cerrar login",
            command=self.ventana.destroy,
            bootstyle="secondary",
        ).pack(pady=5)
        ttkb.Button(
            self.ventana,
            text="Abrir ventana principal",
            command=vent,
            bootstyle="primary",
        ).pack(pady=5)
      
        self.ventana.mainloop()

    def validar(self):
        usuario = self.usuario_correcto
        contra = self.password_correctowo

objeto = login()
        
        