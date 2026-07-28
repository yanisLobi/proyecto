from copy import deepcopy
from typing import cast

from bson.objectid import ObjectId
from pymongo.collection import Collection

from conexion2 import Conexion


def _obtener_coleccion(nombre_tabla=None):
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
    if isinstance(valor, ObjectId):
        return valor
    if isinstance(valor, str) and ObjectId.is_valid(valor):
        return ObjectId(valor)
    return valor


def _normalizar_documento(documento):
    doc = deepcopy(documento)
    if "_id" in doc:
        doc["id"] = str(doc["_id"])
        del doc["_id"]
    elif "id" in doc:
        doc["id"] = str(doc["id"])
    return doc


def obtener_tabla(nombre_tabla):
    coleccion = _obtener_coleccion(nombre_tabla)
    resultados = [
        _normalizar_documento(doc)
        for doc in coleccion.find({})
    ]
    return resultados


def borrar_registro(nombre_tabla, nombre_columna, valor_columna):
    coleccion = _obtener_coleccion(nombre_tabla)
    valor = _transformar_id(valor_columna) if nombre_columna in ["id", "_id"] else valor_columna
    columna = "_id" if nombre_columna == "id" else nombre_columna
    coleccion.delete_one({columna: valor})


def obtener_registros(nombre_tabla, nombre_columna, valor_columna):
    coleccion = _obtener_coleccion(nombre_tabla)
    valor = _transformar_id(valor_columna) if nombre_columna in ["id", "_id"] else valor_columna
    columna = "_id" if nombre_columna == "id" else nombre_columna

    resultados = [
        _normalizar_documento(doc)
        for doc in coleccion.find({columna: valor})
    ]
    return resultados


def insertar_registro(tabla, diccionario_usuario):
    coleccion = _obtener_coleccion(tabla)
    documento = deepcopy(diccionario_usuario)

    if "id" in documento and documento["id"]:
        documento["_id"] = _transformar_id(documento["id"])
        del documento["id"]

    coleccion.insert_one(documento)


def actualizar_registro(tabla, diccionario_usuario, nombre_columna, valor_columna):
    coleccion = _obtener_coleccion(tabla)
    documento = deepcopy(diccionario_usuario)

    if "id" in documento:
        del documento["id"]

    valor = _transformar_id(valor_columna) if nombre_columna in ["id", "_id"] else valor_columna
    columna = "_id" if nombre_columna == "id" else nombre_columna

    coleccion.update_one({columna: valor}, {"$set": documento})


def obtener_valores(nombre_tabla, nombre_columna, nombre_columna1, nombre_columna2):
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


def obtener_valores_usuarios(nombre_columna, nombre_columna1, nombre_columna2, tipo_usuario):
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
    coleccion = _obtener_coleccion(nombre_tabla)
    columna = "_id" if columna_condicion == "id" else columna_condicion
    valor = _transformar_id(valor_condicion) if columna in ["_id", "id"] else valor_condicion

    resultados = [
        _normalizar_documento(doc)
        for doc in coleccion.find({columna: valor})
    ]
    return resultados
