from .conexion_mysql import conectar


def obtener_tabla(nombre_tabla, solo_activos=True):
    """Recupera todos los registros de la tabla indicada.
    Si solo_activos es True, muestra únicamente los que están marcados como activos."""
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)
    letras = nombre_tabla[:2]
    valor_columna = letras + "_activo"

    if solo_activos:
        query = f"SELECT * FROM {nombre_tabla} WHERE {valor_columna} = 1"
    else:
        query = f"SELECT * FROM {nombre_tabla}"

    print(f"obtener_tabla: {query} \n")
    cursor.execute(query)
    resultados = cursor.fetchall()
    cursor.close()
    conexion.close()
    return resultados


def borrar_registro_fisico(nombre_tabla, nombre_columna, valor_columna):
    """Elimina de forma definitiva un registro de la tabla seleccionada.
    Se usa cuando se quiere quitar algo por completo y no dejarlo como inactivo."""
    conexion = conectar()
    cursor = conexion.cursor()
    query = f"DELETE FROM {nombre_tabla} WHERE {nombre_columna} = {valor_columna}"

    print(f"borrar_registro_fisico: {query} \n")
    cursor.execute(query)
    conexion.commit()
    cursor.close()
    conexion.close()


def borrar_registro(nombre_tabla, nombre_columna, valor_columna):
    """Cambia el estado de un registro a inactivo.
    Sirve para ocultarlo sin borrarlo de la base de datos."""
    letras = nombre_tabla[:2]
    columna_activo = letras + "_activo"

    sql = f"UPDATE {nombre_tabla} set {columna_activo} = 0 WHERE {nombre_columna} = {valor_columna}"
    print(f"borrar_registro: {sql} \n")

    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute(sql)
    conexion.commit()
    cursor.close()
    conexion.close()


def obtener_registros(
        nombre_tabla,
        nombre_columna,
        valor_columna,
        solo_activos=True):
    """Busca los registros que coincidan con un valor en una columna concreta.
    El parámetro solo_activos limita la búsqueda a los elementos que siguen vigentes."""
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)

    letras = nombre_tabla[:2]
    tabla_letras = letras + "_activo"

    if solo_activos:
        query = f"SELECT * FROM {nombre_tabla} WHERE {nombre_columna} = {valor_columna} AND {tabla_letras} = 1"
    else:
        query = f"SELECT * FROM {nombre_tabla} WHERE {nombre_columna} = {valor_columna}"
    print(f"obtener_registros: {query} \n")

    cursor.execute(query)
    resultados = cursor.fetchall()
    cursor.close()
    conexion.close()
    return resultados


def insertar_registro(tabla, diccionario_usuario):
    """Guarda un nuevo registro en la tabla indicada.
    El diccionario debe contener los nombres de las columnas y los valores que se van a guardar."""
    usuario_keys = ", ".join(diccionario_usuario.keys())
    separadores = ", %s" * len(diccionario_usuario.values())
    sql = f"INSERT INTO {tabla} ({usuario_keys}) VALUES ({separadores[1:]})"
    print(f"insertar_registro: {sql} \n")

    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute(sql, tuple(diccionario_usuario.values()))
    id_generado = cursor.lastrowid
    conexion.commit()
    cursor.close()
    conexion.close()

    return id_generado


def insertar_receta(id_tratamiento, id_medicamento):
    """Relaciona un tratamiento con un medicamento.
    Se usa para guardar esa conexión en la tabla de recetas."""
    conexion = conectar()
    cursor = conexion.cursor()

    sql = """
        INSERT INTO receta (id_tratamiento, id_medicamento)
        VALUES (%s, %s)
    """
    print(f"insertar_receta {sql} \n")
    cursor.execute(sql, (id_tratamiento, id_medicamento))
    conexion.commit()
    cursor.close()
    conexion.close()


def actualizar_registro(
        tabla,
        diccionario_usuario,
        nombre_columna,
        valor_columna):
    """Modifica los datos de un registro ya existente.
    El diccionario incluye los campos que se van a cambiar y el valor de búsqueda para encontrar el registro."""
    usuario_keys = "=%s, ".join(diccionario_usuario.keys())

    sql = f"UPDATE {tabla} set {usuario_keys} =%s WHERE {nombre_columna} = {valor_columna}"
    print(f"Obeniendo tabla: {sql} \n")

    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute(sql, tuple(diccionario_usuario.values()))
    conexion.commit()
    cursor.close()
    conexion.close()


def obtener_valores(
        nombre_tabla,
        nombre_columna,
        nombre_columna1,
        nombre_columna2,
        solo_activos=True):
    """Extrae algunos campos específicos de una tabla para mostrarlos.
    Es útil cuando no se necesitan todos los datos, solo los más importantes."""
    conexion = conectar()
    cursor = conexion.cursor()

    letras = nombre_tabla[:2]
    filtro_activo = f" WHERE {letras}_activo = 1" if solo_activos else ""
    query = f"SELECT {nombre_columna}, {nombre_columna1}, {nombre_columna2} FROM {nombre_tabla}{filtro_activo}"
    print(f"obtener_valores: {query} \n")

    cursor.execute(query)
    resultados = cursor.fetchall()
    cursor.close()
    conexion.close()
    return resultados


def obtener_valores_medicamentos(
        nombre_tabla,
        nombre_columna,
        nombre_columna1,
        solo_activos=True):
    """Devuelve información básica de los medicamentos.
    Se usa para llenar listas o combos sin cargar toda la tabla."""
    conexion = conectar()
    cursor = conexion.cursor()

    letras = nombre_tabla[:2]
    filtro_activo = f" WHERE {letras}_activo = 1" if solo_activos else ""
    query = f"SELECT {nombre_columna}, {nombre_columna1} FROM {nombre_tabla}{filtro_activo}"
    print(f"obtener_valores_medicamentos: {query} \n")

    cursor.execute(query)
    resultados = cursor.fetchall()
    cursor.close()
    conexion.close()
    return resultados


def obtener_valores_usuarios(
        nombre_columna,
        nombre_columna1,
        nombre_columna2,
        tipo_usuario,
        solo_activos=True):
    """Recupera datos de usuarios según su tipo.
    Esto ayuda a mostrar, por ejemplo, solo doctores o solo enfermeras."""
    conexion = conectar()
    cursor = conexion.cursor()

    filtro_activo = " AND us_activo = 1" if solo_activos else ""
    query = f"SELECT {nombre_columna}, {nombre_columna1}, {nombre_columna2} FROM usuarios WHERE us_tipo_usuario = '{tipo_usuario}'{filtro_activo}"
    print(f"obtener_valores_usuarios: {query} \n")

    cursor.execute(query)
    resultados = cursor.fetchall()
    cursor.close()
    conexion.close()
    return resultados


def obtener_medicinas_de_tratamientos(id_tratamiento):
    """Encuentra los medicamentos asociados a un tratamiento.
    El id_tratamiento sirve como clave para buscar esa relación."""
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)

    consulta = """
        SELECT m.*
        FROM medicamentos m
        INNER JOIN receta r
            ON m.id_medicamentos = r.id_medicamento
        WHERE m.me_activo = 1 AND r.id_tratamiento = %s
    """
    print(f"obtener_medicinas_de_tratamientos {consulta} \n")

    cursor.execute(consulta, (id_tratamiento,))
    medicamentos = cursor.fetchall()
    cursor.close()
    conexion.close()
    return medicamentos


def eliminar_recetas_tratamiento(id_tratamiento):
    """Quita todas las relaciones de medicamentos de un tratamiento.
    Se usa antes de actualizar o borrar un tratamiento completo."""
    conexion = conectar()
    cursor = conexion.cursor()

    sql = """
        DELETE FROM receta
        WHERE id_tratamiento = %s
    """
    print(f"eliminar_recetas_tratamiento: {sql} \n")

    cursor.execute(sql, (id_tratamiento,))
    conexion.commit()
    cursor.close()
    conexion.close()


def obtener_valores_recetas(id_tratamiento):
    """Muestra qué medicamentos están ligados a un tratamiento.
    Sirve para ver la lista de recetas relacionadas con ese registro."""
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)

    consulta = """
        SELECT
            r.id_tratamiento,
            t.tr_nombre,
            r.id_medicamento,
            m.me_nombre_comercial
        FROM receta r
        INNER JOIN tratamientos t
            ON r.id_tratamiento = t.id_tratamientos
        INNER JOIN medicamentos m
            ON r.id_medicamento = m.id_medicamentos
        WHERE r.id_tratamiento = %s
    """
    print(f"obtener_valores_recetas: {consulta} \n")

    cursor.execute(consulta, (id_tratamiento,))
    recetas = cursor.fetchall()
    cursor.close()
    conexion.close()
    return recetas


def obtener_pacientes_doctor(id_doctor):
    """Busca los pacientes que pertenecen a un doctor.
    El id_doctor se usa como filtro para encontrar esa relación."""
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)

    consulta = """
        SELECT DISTINCT p.*
        FROM pacientes p
        INNER JOIN tratamientos t
            ON p.id_pacientes = t.id_paciente
        WHERE t.tr_activo =1 AND p.pa_activo =1 AND t.id_doctor = %s
    """
    print(f"obtener_pacientes_doctor: {consulta} \n")

    cursor.execute(consulta, (id_doctor,))
    pacientes = cursor.fetchall()
    cursor.close()
    conexion.close()
    return pacientes


def obtener_tratamientos_enfermera(id_enfermera_principal):
    """Encuentra los tratamientos asignados a una enfermera.
    El id_enfermera_principal permite filtrar por la persona encargada."""
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)

    consulta = """
        SELECT DISTINCT t.*
        FROM tratamientos t
        INNER JOIN pacientes p
            ON p.id_pacientes = t.id_paciente
        WHERE t.tr_activo =1 AND p.pa_activo =1 AND p.id_enfermera_principal = %s
    """
    print(f"obtener_tratamientos_enfermera: {consulta} \n")
    cursor.execute(consulta, (id_enfermera_principal,))
    registros = cursor.fetchall()

    cursor.close()
    conexion.close()
    print(f"Tratamientos: {consulta}")
    return registros


def obtener_ids_tratamientos_visibles(tipo_usuario, id_usuario):
    """Devuelve los tratamientos que un usuario puede ver.
    Dependiendo del tipo de usuario, ya que un tratamiento si tiene id_doctor 
    pero enfermera ocupa revisar los pacientes que tiene asignados."""
    if tipo_usuario == "Administrador":
        return None
    if tipo_usuario == "Doctor":
        tratamientos = obtener_registros(
            "tratamientos", "id_doctor", id_usuario, False)
    elif tipo_usuario == "Enfermera":
        tratamientos = obtener_tratamientos_enfermera(id_usuario)
    else:
        tratamientos = []
    return {str(t.get("id_tratamientos")) for t in tratamientos}
