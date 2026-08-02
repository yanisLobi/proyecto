from conexion import conectar


def obtener_tabla(nombre_tabla, solo_activos=True):
    conexion = conectar()

    cursor = conexion.cursor(dictionary=True)
    letras = nombre_tabla[:2]
    valor_columna = letras + "_activo"
    if solo_activos:
        query = f"SELECT * FROM {nombre_tabla} WHERE {valor_columna} = 1"
    else:
        query = f"SELECT * FROM {nombre_tabla}"

    cursor.execute(query)
    resultados = cursor.fetchall()
    cursor.close()
    conexion.close()
    return resultados


def borrar_registro_fisico(nombre_tabla, nombre_columna, valor_columna):
    conexion = conectar()

    cursor = conexion.cursor()

    query = f"DELETE FROM {nombre_tabla} WHERE {nombre_columna} = {valor_columna}"

    cursor.execute(query)
    conexion.commit()
    cursor.close()
    conexion.close()


def borrar_registro(nombre_tabla, nombre_columna, valor_columna):
    letras = nombre_tabla[:2]
    columna_activo = letras + "_activo"

    sql = f"UPDATE {nombre_tabla} set {columna_activo} = 0 WHERE {nombre_columna} = {valor_columna}"

    conexion = conectar()

    cursor = conexion.cursor()

    cursor.execute(sql)

    conexion.commit()

    cursor.close()
    conexion.close()


def obtener_registros(nombre_tabla, nombre_columna, valor_columna):
    conexion = conectar()

    cursor = conexion.cursor(dictionary=True)

    query = f"SELECT * FROM {nombre_tabla} WHERE {nombre_columna} = {valor_columna}"

    cursor.execute(query)
    resultados = cursor.fetchall()
    cursor.close()
    conexion.close()
    return resultados


def insertar_registro(tabla, diccionario_usuario):
    usuario_keys = ", ".join(diccionario_usuario.keys())
    separadores = ", %s" * len(diccionario_usuario.values())
    sql = f"INSERT INTO {tabla} ({usuario_keys}) VALUES ({separadores[1:]})"

    conexion = conectar()

    cursor = conexion.cursor()

    cursor.execute(sql, tuple(diccionario_usuario.values()))
    
    id_generado = cursor.lastrowid
    
    conexion.commit()

    cursor.close()
    conexion.close()
    
    return id_generado

def insertar_receta(id_tratamiento, id_medicamento):
    conexion = conectar()

    cursor = conexion.cursor()

    sql = """
        INSERT INTO receta (id_tratamiento, id_medicamento)
        VALUES (%s, %s)
    """

    cursor.execute(sql, (id_tratamiento, id_medicamento))

    conexion.commit()

    cursor.close()
    conexion.close()

def actualizar_registro(tabla, diccionario_usuario, nombre_columna, valor_columna):
    usuario_keys = "=%s, ".join(diccionario_usuario.keys())

    sql = f"UPDATE {tabla} set {usuario_keys} =%s WHERE {nombre_columna} = {valor_columna}"

    conexion = conectar()

    cursor = conexion.cursor()

    cursor.execute(sql, tuple(diccionario_usuario.values()))

    conexion.commit()

    cursor.close()
    conexion.close()


def obtener_valores(nombre_tabla, nombre_columna, nombre_columna1, nombre_columna2, solo_activos=True):
    conexion = conectar()

    cursor = conexion.cursor()

    letras = nombre_tabla[:2]
    filtro_activo = f" WHERE {letras}_activo = 1" if solo_activos else ""
    query = f"SELECT {nombre_columna}, {nombre_columna1}, {nombre_columna2} FROM {nombre_tabla}{filtro_activo}"

    cursor.execute(query)
    resultados = cursor.fetchall()
    cursor.close()
    conexion.close()
    return resultados

def obtener_valores_medicamentos(nombre_tabla, nombre_columna, nombre_columna1, solo_activos=True):
    conexion = conectar()

    cursor = conexion.cursor()

    letras = nombre_tabla[:2]
    filtro_activo = f" WHERE {letras}_activo = 1" if solo_activos else ""
    query = f"SELECT {nombre_columna}, {nombre_columna1} FROM {nombre_tabla}{filtro_activo}"

    cursor.execute(query)
    resultados = cursor.fetchall()
    cursor.close()
    conexion.close()
    return resultados


def obtener_valores_usuarios(nombre_columna, nombre_columna1, nombre_columna2, tipo_usuario, solo_activos=True):
    conexion = conectar()

    cursor = conexion.cursor()

    filtro_activo = " AND us_activo = 1" if solo_activos else ""
    query = f"SELECT {nombre_columna}, {nombre_columna1}, {nombre_columna2} FROM usuarios WHERE us_tipo_usuario = '{tipo_usuario}'{filtro_activo}"

    cursor.execute(query)
    resultados = cursor.fetchall()
    cursor.close()
    conexion.close()
    return resultados


def obtener_tabla_condicion(nombre_tabla, columna_condicion, valor_condicion):
    conexion = conectar()

    cursor = conexion.cursor(dictionary=True)

    query = f"SELECT * FROM {nombre_tabla} WHERE {columna_condicion} = '{valor_condicion}'"

    cursor.execute(query)
    resultados = cursor.fetchall()
    cursor.close()
    conexion.close()
    return resultados


def obtener_medicinas_de_tratamientos(id_tratamiento):
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)

    consulta = """
        SELECT m.*
        FROM medicamentos m
        INNER JOIN receta r
            ON m.id_medicamentos = r.id_medicamento
        WHERE r.id_tratamiento = %s
    """

    cursor.execute(consulta, (id_tratamiento,))
    medicamentos = cursor.fetchall()

    cursor.close()
    conexion.close()

    return medicamentos

def eliminar_recetas_tratamiento(id_tratamiento):
    conexion = conectar()
    cursor = conexion.cursor()

    sql = """
        DELETE FROM receta
        WHERE id_tratamiento = %s
    """

    cursor.execute(sql, (id_tratamiento,))
    conexion.commit()

    cursor.close()
    conexion.close()
    

    

def obtener_valores_recetas(id_tratamiento):
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

    cursor.execute(consulta, (id_tratamiento,))
    recetas = cursor.fetchall()

    cursor.close()
    conexion.close()

    return recetas

def obtener_pacientes_doctor(id_doctor):
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)

    consulta = """
        SELECT p.*
        FROM pacientes p
        INNER JOIN tratamientos t
            ON p.id_pacientes = t.id_paciente
        WHERE t.tr_activo =1 AND p.pa_activo =1 AND t.id_doctor = %s
    """

    cursor.execute(consulta, (id_doctor,))
    pacientes = cursor.fetchall()

    cursor.close()
    conexion.close()
    print(f"obtener pacientes doctor: {consulta}")
    return pacientes
