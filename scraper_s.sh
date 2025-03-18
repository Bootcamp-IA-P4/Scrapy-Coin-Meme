#!/usr/bin/env bash

# Añadir el directorio "app" al PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:app"

# Función para mostrar el uso del script
usage() {
    echo "Uso: $0 [-sp]"
    echo "Opciones:"
    echo "  -sp    Ejecutar script-cron.py"
}

# Comprobar el argumento proporcionado
case "$1" in
    -sp) 
        python3 -m venv /root/.venv
        python3 /app/script-cron.py 
        ;;
    *) 
        echo "Opción no válida."
        usage
        ;;
esac