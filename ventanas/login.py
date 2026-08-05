import tkinter as tk
from tkinter import messagebox

from conexion import conectar
from ventanas.aplicacion import iniciar_aplicacion
from ventanas.registro import iniciar_registro
from db_mysql import obtener_tabla
import ttkbootstrap as ttkb
from seguridad import verificar_contrasena
from herramients import agregar_boton_mostrar_contrasena


def main():
    # temas: minty (verde), cosmo (blanco), darkly (obscuro)
    ventana = ttkb.Window(themename="minty")
    ventana.title("AbueCare Login")
    ventana.geometry("360x550")
    ventana.pack_propagate(False)
    ventana.resizable(False, False)
    imagen_original = tk.PhotoImage(file="recursos/1.png")
    ventana.iconphoto(True, imagen_original)

    imagen_original = tk.PhotoImage(file="recursos/1.png")
    imagen_pequena = imagen_original.subsample(10)

    etiqueta_logo = ttkb.Label(ventana, image=imagen_pequena)
    etiqueta_logo.pack(pady=(50, 30))

    contenido_frame = ttkb.Frame(ventana)
    contenido_frame.pack(padx=30, fill="x")
    contenido_frame.grid_columnconfigure(0, weight=1)
    contenido_frame.grid_columnconfigure(1, weight=0)
    
    contenido_frame2 = ttkb.Frame(contenido_frame)
    contenido_frame2.grid(row=3, column=0, sticky="ew", pady=(0, 30))
    contenido_frame2.grid_columnconfigure(0, weight=10)
    contenido_frame2.grid_columnconfigure(1, weight=1)

    # Entry para correo
    ttkb.Label(
        contenido_frame,
        text="Correo:").grid(
        row=0,
        column=0,
        sticky="w",
        pady=(
            5,
            2))
    correo = ttkb.Entry(contenido_frame)
    correo.grid(row=1, column=0, sticky="ew", pady=(0, 10))

    # Entry para contraseña
    ttkb.Label(
        contenido_frame,
        text="Contraseña:").grid(
        row=2,
        column=0,
        sticky="w",
        pady=(
            5,
            2))
    contra = ttkb.Entry(contenido_frame2, show="*")
    contra.grid(row=3, column=0, sticky="ew", pady=(0, 10))
    agregar_boton_mostrar_contrasena(
        contenido_frame2,
        contra,
        row=3,
        column=1,
        sticky="ew",
        padx=(6, 0),
        pady=(0, 10),
        width=3,
    )

    def intentar_login():
        lista_usuarios = obtener_tabla('usuarios')
        correo_introducido = correo.get().strip()
        contrasena_introducida = contra.get().strip()

        if correo_introducido == "":
            messagebox.showinfo(
                "Error al iniciar sesion",
                "Debes introducir correo y contraseña")
            return

        correos = [usuario.get("us_correo_electronico")
                   for usuario in lista_usuarios]
        print(f"Correos encontrados en la DB: {correos}")

        if correo_introducido not in correos:
            messagebox.showinfo(
                "Error al iniciar sesion",
                "El correo introducido no esta registrado")
            return

        contrasena_esperada = [usuario.get("us_contraseña") for usuario in lista_usuarios if usuario.get(
            "us_correo_electronico") == correo_introducido][0]
        print(f"Contraseña encontrada en la DB: {contrasena_esperada}")

        """ if contrasena_introducida != contrasena_esperada:
            messagebox.showinfo("Error al iniciar sesion", "La contrasena es incorrecta")
            return """

        if not verificar_contrasena(
                contrasena_introducida,
                contrasena_esperada):
            messagebox.showinfo(
                "Error al iniciar sesión",
                "La contraseña es incorrecta")
            return

        # Usuario y contraseña correctos:

        usuario = [usuario for usuario in lista_usuarios if usuario.get(
            "us_correo_electronico") == correo_introducido][0]
        nombre_usuario = [usuario.get("us_nombre") for usuario in lista_usuarios if usuario.get(
            "us_correo_electronico") == correo_introducido][0]

        contenido_frame.pack_forget()
        frame_bienvenida = ttkb.Frame(ventana)
        frame_bienvenida.grid_columnconfigure(0, weight=1)
        frame_bienvenida.grid_columnconfigure(1, weight=0)

        ttkb.Label(
            frame_bienvenida,
            text="Inicio de sesión exitoso",
            font=("Arial", 13, "bold"),
            bootstyle="success",
        ).pack(pady=(20, 10))
        ttkb.Label(
            frame_bienvenida,
            text=f"Bienvenido a Abuecare {nombre_usuario}",
            font=("Arial", 8),
            wraplength=260,
            justify="center",
        ).pack(padx=20)

        frame_bienvenida.pack(padx=30, fill="x")

        def avanzar_y_limpiar():
            frame_bienvenida.pack_forget()
            frame_bienvenida.destroy()
            contenido_frame.pack(padx=30, fill="x")
            iniciar_aplicacion(ventana, usuario, contra)
        ventana.after(3000, avanzar_y_limpiar)

    def abrir_registro():
        iniciar_registro(ventana)

    botones_frame = ttkb.Frame(contenido_frame)
    botones_frame.grid(row=4, column=0, sticky="ew", pady=(20, 30))
    botones_frame.grid_columnconfigure(0, weight=1)
    botones_frame.grid_columnconfigure(1, weight=1)

    # Botón 1: Columna 0 ----- Boton de iniciar sesion
    iniciar = ttkb.Button(
        botones_frame,
        text="Iniciar Sesion",
        command=intentar_login,
        bootstyle="primary")
    # que es bootstyle
    iniciar.grid(row=0, column=0, sticky="ew", padx=(0, 8))

    # Botón 2: Columna 1 ----- Boton de registro
    registrar = ttkb.Button(
        botones_frame,
        text="Registrarse",
        command=abrir_registro,
        bootstyle="secondary")
    registrar.grid(row=0, column=1, sticky="ew", padx=(8, 0))

    # Ejecutar la aplicación
    ventana.mainloop()


if __name__ == "__main__":
    main()
