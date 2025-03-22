import secrets
import string
def generar_cadena_aleatoria(longitud=10):
    caracteres = string.ascii_letters + string.digits  # Letras mayúsculas, minúsculas y números
    return ''.join(secrets.choice(caracteres) for _ in range(longitud))