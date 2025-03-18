# Usar la imagen oficial de Python
ARG PYTHON_VERSION=3.10.8
FROM python:${PYTHON_VERSION}-slim as base
#FROM selenium/standalone-chrome:latest 
# Establecer el directorio de trabajo
WORKDIR /app

# Copiar los archivos del proyecto
COPY . /app
#instalar dependencias os
USER root
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    xvfb \
    cron \
    && rm -rf /var/lib/apt/lists/*


# Instalar dependencias py
COPY requirements.txt .
RUN python -m pip install --upgrade pip
RUN python -m pip install --no-cache-dir -r requirements.txt

# Definir variables de entorno para Chromium
ENV CHROMIUM_PATH="/usr/bin/chromium"
ENV CHROMEDRIVER_PATH="/usr/bin/chromedriver"

# Permisos en directorios
RUN mkdir -p /app && \
    chmod -R 777 /app
RUN mkdir -p /app && mkdir -p /var/log

# Copiar archivos al contenedor
COPY script-cron.py /app/script-cron.py
RUN chmod +x /app/script-cron.py

COPY scraper_s.sh /app/scraper_s.sh
RUN chmod +x /app/scraper_s.sh

COPY . .
# EStablecer el horario de cron
RUN echo "* * * * * export DISPLAY=:1 && /usr/bin/python3 /app/script-cron.py >> /var/log/cron.log 2>&1" > /etc/cron.d/cronfile
#RUN echo "* * * * * sh /app/scraper_s.sh -sp >> /var/log/cron.log 2>&1" > /etc/cron.d/cronfile    

# Dar permisos a los archivos cronfile
RUN chmod 0644 /etc/cron.d/cronfile && \
    crontab /etc/cron.d/cronfile   



# Exponer el puerto 8000
EXPOSE 8000

# ejecutar script sh
#COPY start.sh /start.sh
#RUN chmod +x /start.sh
#CMD ["/start.sh"]
CMD service cron start && uvicorn main:app --host 0.0.0.0 --port 8000 --reload
