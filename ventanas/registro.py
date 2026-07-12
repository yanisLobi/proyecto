import tkinter as tk

        
def iniciar_registro(ventana_login):
    # Ocultamos la ventana que nos llamó (la ventana de inicio de sesion)
    ventana_login.withdraw()
    ventana = tk.Toplevel()
    ventana.title("AbueCare Registro")
    ventana.geometry("500x700")

    ventana.protocol("WM_DELETE_WINDOW", ventana_login.destroy)

    def cerrar_sesion():
        ventana.destroy()          # Cierra por completo el Dashboard
        ventana_login.deiconify()  # Hace visible otra vez el Login
        
    # Entry para correo
    tk.Label(ventana, text="Correo:").pack(pady=5)
    correo = tk.Entry(ventana, width=30)
    correo.pack(pady=5)

    # Entry para contraseña
    tk.Label(ventana, text="Contraseña:").pack(pady=5)
    contra = tk.Entry(ventana, width=30)
    contra.pack(pady=5)
    
    # Entry para contraseña
    tk.Label(ventana, text="Repite la contraseña:").pack(pady=5)
    contra = tk.Entry(ventana, width=30)
    contra.pack(pady=5)

    # Boton para regresar al inicio de sesion (cancelar registro)
    tk.Button(ventana, text="Cancelar", command=cerrar_sesion).pack()

    # Ejecutar la aplicación
    ventana.mainloop()

if __name__ == "__main__":
    pass
