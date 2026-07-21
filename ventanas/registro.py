import tkinter as tk
from tkinter import messagebox

from crud.usuarios.crearUsuarios import CrearUsuario
from herramientas import insertar_registro


def iniciar_registro(ventana_login):
    # Ocultamos la ventana que nos llamó (la ventana de inicio de sesion)
    ventana_login.withdraw()
    ventana = tk.Toplevel()
    ventana.title("AbueCare Registro")
    ventana.geometry("900x650")

    ventana.protocol("WM_DELETE_WINDOW", ventana_login.destroy)

    def cerrar_registro():
        ventana.destroy()          # Cierra por completo el Dashboard
        ventana_login.deiconify()  # Hace visible otra vez el Login

    class RegistroUsuario(CrearUsuario):
        def ir_lista(self):
            cerrar_registro()

        def crear_usuario(self):
            self.guardar_valores()
            insertar_registro(self.tabla, self.nuevo_registro)
            messagebox.showinfo("Crear", "Se creó correctamente el usuario")
            cerrar_registro()

    RegistroUsuario(ventana, titulo="Registro")

    # Ejecutar la aplicación
    ventana.mainloop()

if __name__ == "__main__":
    pass
