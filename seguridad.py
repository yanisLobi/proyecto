import bcrypt


def encriptar_contrasena(contrasena):
    """Convierte una contraseña en una versión protegida.
    Genera un valor seguro para guardar la información sin mostrarla en texto claro."""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(
        contrasena.encode("utf-8"),
        salt
    ).decode("utf-8")


def verificar_contrasena(contrasena, hash_guardado):
    """Comprueba si una contraseña coincide con su valor protegido.
    Devuelve True cuando ambos valores representan la misma clave."""
    return bcrypt.checkpw(
        contrasena.encode("utf-8"),
        hash_guardado.encode("utf-8")
    )
