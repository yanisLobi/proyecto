from copy import deepcopy
from typing import cast

from bson.objectid import ObjectId
from pymongo.collection import Collection

from .conexion_mongo import Conexion
from .db_mysql import obtener_registros as obtener_registros_mysql


def _obtener_coleccion(nombre_tabla=None):
    """Abre la conexión a MongoDB y devuelve la colección pedida.
    Si no se pasa un nombre, usa la colección por defecto configurada en la conexión."""
    conexion = Conexion()
    if conexion.error:
        raise conexion.error

    if conexion.db is None:
        raise Exception("No se pudo conectar a MongoDB")

    if nombre_tabla:
        return cast(Collection, conexion.db[nombre_tabla])

    coleccion = conexion.obtener_coleccion()
    if coleccion is None:
        raise Exception("No se pudo obtener la colección de MongoDB")

    return cast(Collection, coleccion)


def _transformar_id(valor):
    """Convierte un texto que parece ser un ID de Mongo en un ObjectId real.
    Esto ayuda a buscar documentos correctamente cuando el valor viene como cadena."""
    if isinstance(valor, ObjectId):
        return valor
    if isinstance(valor, str) and ObjectId.is_valid(valor):
        return ObjectId(valor)
    return valor


def _normalizar_documento(documento):
    """Cambia el formato del documento para que sea más fácil de usar en la app.
    Convierte el campo _id a id y deja el resto del contenido igual."""
    doc = deepcopy(documento)
    if "_id" in doc:
        doc["id"] = str(doc["_id"])
        del doc["_id"]
    elif "id" in doc:
        doc["id"] = str(doc["id"])
    return doc


def _convertir_id_tratamiento(valor):
    """Convierte los IDs de tratamientos que llegan como texto a números enteros.
    Esto evita problemas al comparar valores en MongoDB."""
    if isinstance(valor, str) and valor.isdigit():
        return int(valor)
    return valor


def _obtener_eventos_por_tratamientos(id_tratamientos):
    """Busca los eventos de consulta relacionados con varios tratamientos.
    Recibe una lista de IDs y devuelve los documentos que coinciden con ellos."""
    if not id_tratamientos:
        return []

    coleccion = _obtener_coleccion("consultas")
    ids_convertidos = [
        _convertir_id_tratamiento(valor)
        for valor in id_tratamientos
        if valor is not None
    ]
    if not ids_convertidos:
        return []
    #print(f"_obtener_eventos_por_tratamientos {ids_convertidos}")

    registros = list(coleccion.find({"id_tr": {"$in": ids_convertidos}}))
    
        
    #print(f"encontrados {registros}")

    return [_normalizar_documento(doc) for doc in registros]


def obtener_tabla(nombre_tabla):
    """Trae todos los documentos de una colección concreta de MongoDB.
    El nombre de la colección debe indicarse claramente para no buscar en la equivocada."""
    coleccion = _obtener_coleccion(nombre_tabla)
    resultados = [
        _normalizar_documento(doc)
        for doc in coleccion.find({})
    ]
    return resultados


def borrar_registro(nombre_tabla, nombre_columna, valor_columna):
    """Elimina un documento de una colección según una columna y un valor.
    El parámetro nombre_columna indica dónde buscar, y valor_columna es el dato a comparar."""
    coleccion = _obtener_coleccion(nombre_tabla)
    valor = _transformar_id(valor_columna) if nombre_columna in [
        "id", "_id"] else valor_columna
    columna = "_id" if nombre_columna == "id" else nombre_columna
    coleccion.delete_one({columna: valor})


def obtener_registros(nombre_tabla, nombre_columna, valor_columna):
    """Busca documentos que coincidan con un valor en una columna específica.
    Sirve para recuperar registros relacionados con un mismo criterio de búsqueda."""
    coleccion = _obtener_coleccion(nombre_tabla)
    valor = _transformar_id(valor_columna) if nombre_columna in [
        "id", "_id"] else valor_columna
    columna = "_id" if nombre_columna == "id" else nombre_columna

    resultados = [
        _normalizar_documento(doc)
        for doc in coleccion.find({columna: valor})
    ]
    return resultados


def obtener_eventos_doctor(id_doctor):
    """Obtiene los eventos asociados a los tratamientos de un doctor.
    Usa el ID del doctor para encontrar primero sus tratamientos y luego sus consultas."""
    tratamientos = obtener_registros_mysql(
        "tratamientos", "id_doctor", id_doctor)
    ids_tratamientos = [
        trat.get("id_tratamientos")
        for trat in tratamientos
        if trat.get("id_tratamientos") is not None
    ]
    #print(f"obtener_eventos_doctor {ids_tratamientos}")
    return _obtener_eventos_por_tratamientos(ids_tratamientos)


def obtener_eventos_enfermera(id_enfermera):
    """Busca los eventos relacionados con los pacientes de una enfermera.
    Recorre los pacientes y luego obtiene los tratamientos vinculados a cada uno."""
    pacientes = obtener_registros_mysql(
        "pacientes", "id_enfermera_principal", id_enfermera)
    ids_tratamientos = []
    for paciente in pacientes:
        id_paciente = paciente.get("id_pacientes")
        if id_paciente is None:
            continue
        tratamientos = obtener_registros_mysql(
            "tratamientos", "id_paciente", id_paciente)
        ids_tratamientos.extend(
            trat.get("id_tratamientos")
            for trat in tratamientos
            if trat.get("id_tratamientos") is not None
        )
    #print(f"obtener_eventos_enfermeras {ids_tratamientos}")
    
    return _obtener_eventos_por_tratamientos(ids_tratamientos)


def insertar_registro(tabla, diccionario_usuario):
    """Guarda un nuevo documento en la colección indicada.
    El diccionario debe contener los campos y valores que se quieren almacenar."""
    coleccion = _obtener_coleccion(tabla)
    documento = deepcopy(diccionario_usuario)

    if "id" in documento and documento["id"]:
        documento["_id"] = _transformar_id(documento["id"])
        del documento["id"]

    coleccion.insert_one(documento)


def actualizar_registro(
        tabla,
        diccionario_usuario,
        nombre_columna,
        valor_columna):
    """Modifica un documento existente usando una condición de búsqueda.
    El valor de nombre_columna y valor_columna sirve para localizar el registro correcto."""
    coleccion = _obtener_coleccion(tabla)
    documento = deepcopy(diccionario_usuario)

    if "id" in documento:
        del documento["id"]

    valor = _transformar_id(valor_columna) if nombre_columna in [
        "id", "_id"] else valor_columna
    columna = "_id" if nombre_columna == "id" else nombre_columna

    coleccion.update_one({columna: valor}, {"$set": documento})


def obtener_valores(
        nombre_tabla,
        nombre_columna,
        nombre_columna1,
        nombre_columna2):
    """Extrae tres campos concretos de cada documento de una colección.
    Se usa cuando solo se necesitan algunos datos para mostrar en pantalla."""
    coleccion = _obtener_coleccion(nombre_tabla)
    resultados = []
    for doc in coleccion.find({}):
        doc_n = _normalizar_documento(doc)
        resultados.append((
            doc_n.get(nombre_columna),
            doc_n.get(nombre_columna1),
            doc_n.get(nombre_columna2),
        ))
    return resultados


def obtener_valores_usuarios(
        nombre_columna,
        nombre_columna1,
        nombre_columna2,
        tipo_usuario):
    """Recupera datos básicos de los usuarios según su tipo.
    Permite filtrar, por ejemplo, solo doctores o solo enfermeras."""
    coleccion = _obtener_coleccion("usuarios")
    resultados = []
    for doc in coleccion.find({"us_tipo_usuario": tipo_usuario}):
        doc_n = _normalizar_documento(doc)
        resultados.append((
            doc_n.get(nombre_columna),
            doc_n.get(nombre_columna1),
            doc_n.get(nombre_columna2),
        ))
    return resultados


def obtener_tabla_condicion(nombre_tabla, columna_condicion, valor_condicion):
    """Busca documentos de una colección usando una condición específica.
    Es parecido a una búsqueda filtrada por un campo y un valor concreto."""
    coleccion = _obtener_coleccion(nombre_tabla)
    columna = "_id" if columna_condicion == "id" else columna_condicion
    valor = _transformar_id(valor_condicion) if columna in [
        "_id", "id"] else valor_condicion

    resultados = [
        _normalizar_documento(doc)
        for doc in coleccion.find({columna: valor})
    ]
    return resultados
