# Usar la imagen oficial de Python
ARG PYTHON_VERSION=3.11.11
FROM python:${PYTHON_VERSION}-slim as builder
#FROM python:3.10.8-slim
#FROM selenium/standalone-chrome:latest 
# Establecer el directorio de trabajo
# Prevents Python from writing pyc files and keeps Python from buffering stdout and stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app

# Copiar los archivos del proyecto
#COPY . /app
#instalar dependencias os
USER root
RUN apt-get update && apt-get install -y \
#    chromium \
#    chromium-driver \
    cron \
    curl \
    wget \
    xvfb \
    unzip \
    firefox-esr \
    libx11-xcb1 \
    libxtst6 \
    libxrender1 \
    libdbus-glib-1-2 \
    libgtk-3-0 \
    libasound2 \
    fonts-liberation \
    libgl1-mesa-dri \
    libpci3 \
    && rm -rf /var/lib/apt/lists/*
# para evitar errores
RUN mkdir -p /tmp/cache/fontconfig && chmod 777 /tmp/cache/fontconfig
ENV FONTCONFIG_PATH=/tmp/cache/fontconfig
# Download and install GeckoDriver
RUN case $(dpkg --print-architecture) in \
    amd64) ARCH=linux64 ;; \
    arm64) ARCH=linux-aarch64 ;; \
    *) echo "Unsupported architecture" && exit 1 ;; \
    esac && \
    wget -O /tmp/geckodriver.tar.gz https://github.com/mozilla/geckodriver/releases/download/v0.35.0/geckodriver-v0.35.0-$ARCH.tar.gz && \
    tar -xvzf /tmp/geckodriver.tar.gz -C /usr/local/bin/ && \
    chmod +x /usr/local/bin/geckodriver && \
    rm /tmp/geckodriver.tar.gz

# Instalar dependencias py
RUN python -m pip install --upgrade pip
COPY requirements.txt /app/
RUN python -m pip install --no-cache-dir -r requirements.txt

# Definir variables de entorno 
#ENV CHROMIUM_PATH="/usr/bin/chromium"
ENV CHROMEDRIVER_PATH="/usr/local/bin/geckodriver"


# Permisos en directorios
RUN mkdir -p /app && \
    chmod -R 777 /app
RUN mkdir -p /var/log

# Copiar archivos/scripts al contenedor
COPY script-cron_dolar.py /app/script-cron_dolar.py
RUN chmod +x /app/script-cron_dolar.py
COPY  script-cron_coin.py /app/script-cron_coin.py
RUN chmod  +x /app/script-cron_coin.py


COPY . .
# EStablecer el horario de cron
ENV PATH="/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin:/usr/bin:/bin:/sbin:/usr/sbin:/usr/local/bin:/usr/local/sbin:/usr/bin:/bin:/sbin"
RUN echo "*/10 * * * * DISPLAY=unix:0.0 /usr/local/bin/python /app/script-cron_dolar.py >> /var/log/cron.log 2>&1" > /etc/cron.d/cronfile_d 
RUN echo "*/10 * * * * DISPLAY=unix:0.0 /usr/local/bin/python /app/script-cron_coin.py >> /var/log/cron.log 2>&1" >> /etc/cron.d/cronfile_d

# Dar permisos a los archivos cronfile
RUN chmod 0644 /etc/cron.d/cronfile_d && \
    crontab /etc/cron.d/cronfile_d



# Exponer el puerto 8000
EXPOSE 8000

# ejecutar script sh
#COPY start.sh /start.sh
#RUN chmod +x /start.sh
#CMD ["/start.sh"]
#CMD service cron start && uvicorn main:app --host 0.0.0.0 --port 8000 --reload
CMD ["sh", "-c", "service cron start && uvicorn main:app --host 0.0.0.0 --port 8000 --reload"]