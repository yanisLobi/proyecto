


def navegar_a_pagina(frame, nombre_clase: str):
    from crud.pacientes.listaPacientes import ListaPacientes
    from crud.pacientes.crearPacientes import CrearPacientes
    from crud.usuarios.listaUsuarios import ListaUsuarios

    paginas = {
        "Lista pacientes": ListaPacientes,
        "Lista usuarios": ListaUsuarios,
        "Crear pacientes": CrearPacientes,
        
       
    }

    for widget in frame.winfo_children():
        widget.destroy()

    paginas[nombre_clase](frame)


       