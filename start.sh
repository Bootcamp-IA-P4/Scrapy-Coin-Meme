#!/bin/sh
echo "Iniciando cron..."
# Dar permisos de ejecución al script de cron
#chmod 0644 /etc/cron.d/cronfile
#crontab /etc/cron.d/cronfile
#touch /var/log/cron.log
#crontab /etc/cron.d/cronfile
# Forzar la eliminación del archivo PID#
#rm -rf /var/run/crond.pid /run/crond.pid

# Iniciar el servicio cron en segundo plano
exec service cron start &
#cron
#cron -L 15 -f &

echo "Cron iniciado."
# Iniciar Uvicorn
echo "Iniciando FastAPI..."
echo python3 --version
exec uvicorn main:app --host 0.0.0.0 --port 8000

