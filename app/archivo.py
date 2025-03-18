
ARCHIVO = "/app/log.txt"
def leer_archivo():
    try:
        with open(ARCHIVO, "r", encoding="utf-8") as archivo:
            contenido = archivo.read()
        #contenido_html = "<br>".join(line.strip() for line in contenido)
        # Retornar el contenido dentro de un HTML básico
        return contenido
    except FileNotFoundError:
        return ("<h1>Error: Archivo no encontrado</h1>")
    except Exception as e:
        return (f"<h1>Error: {e}</h1>")