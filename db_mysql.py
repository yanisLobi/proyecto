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


def obtener_valores(nombre_tabla, nombre_columna, nombre_columna1, nombre_columna2):
    conexion = conectar()

    cursor = conexion.cursor()

    query = f"SELECT {nombre_columna}, {nombre_columna1}, {nombre_columna2} FROM {nombre_tabla} "

    cursor.execute(query)
    resultados = cursor.fetchall()
    cursor.close()
    conexion.close()
    return resultados


def obtener_valores_usuarios(nombre_columna, nombre_columna1, nombre_columna2, tipo_usuario):
    conexion = conectar()

    cursor = conexion.cursor()

    query = f"SELECT {nombre_columna}, {nombre_columna1}, {nombre_columna2} FROM usuarios WHERE us_tipo_usuario = '{tipo_usuario}'"

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
    SELECT
        m.id_medicamentos,
        m.me_nombre_comercial,
        m.me_forma_farmaceutica,
        m.me_concentracion,
        m.me_fecha_caducidad,
        m.me_descripcion,
        m.me_activo
    FROM receta r
    INNER JOIN medicamentos m
        ON r.id_medicamento = m.id_medicamentos
    WHERE r.id_tratamiento = %s
    """

    cursor.execute(consulta, (id_tratamiento,))
    medicamentos = cursor.fetchall()
    cursor.close()
    return medicamentos
