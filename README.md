# Meme Coin Scraping
Dia
## ⚙️ Recommended Technologies
- (⊙_⊙;)**Version Control**: Git / GitHub
- (⊙_⊙;)**Runtime Environment**: Docker
- (⊙_⊙;)**Primary Language**: Python
- (⊙_⊙;)**Useful Libraries**: BeautifulSoup, Scrapy, Requests, Selenium
- (⊙_⊙;)**Databases**: MySQL, PostgreSQL, MongoDB, Firebase
- (⊙_⊙;)**Project Management**: Trello, Jira, GitHub

## 🏆 Niveles de Entrega

### 🟢 Nivel Esencial:
- ✅ Script que accede a un sitio web y extrae información:
    - [Obtención de monedas](https://coinmarketcap.com/es/)
    - [Cambio oficial de dólares a euros](https://www.xe.com/es/currencyconverter/convert/?Amount=1&From=USD&To=EUR)
- ✅ Limpieza y organización de datos.
- ✅ Documentación del código y un README en GitHub.

### 🟡 Nivel Medio:
- ✅ Almacenamiento de los datos en una base de datos estructurada.
    - Limpiea de los datos sobre todo en los importe, pasar de dolar a euro
- ✅ Implementación de logs para trazabilidad del scraper.
- ✅ Tests unitarios para validar el funcionamiento del código.
    Test unitarios:
    1. Connect to database
    2. Create document seguimiento log.txt
    3. Server ON --> requeste 200

### 🟠 Nivel Avanzado:
- ❌ Uso de Programación Orientada a Objetos (OOP) para mejorar la estructura del código.
-  Manejo robusto de errores para evitar bloqueos y baneos de IP.
- ✅ Automatización del scraper para actualizar periódicamente la base de datos con tareas Cron.
    - Obtención de monedas
    - Obtención del Dolar Euro

### 🔴 Nivel Experto:
- ✅ Dockerización completa del proyecto para facilitar despliegue y escalabilidad.
    [Image public](https://hub.docker.com/r/jcmacias/scraping)
- ✅ Implementación de un frontend interactivo para visualizar datos en tiempo real.
- ✅ Despliegue en un servidor accesible públicamente.
    [Enlace despliege](https://scraping-v1-0.onrender.com/)
- ✅ Integración con múltiples sitios web de empleo para mejorar la cantidad y calidad de datos recopilados.

## Prerequisites
- Ensure Docker is running
## important
1. Debe haber una base de datos mongo, el que se referencia desde el .env ejemplo:
    ```sh
    mongodb+srv://user-name:user-password@url-mongodb.net/?retryWrites=true&w=majority&appName=name-database
    ```

## Steps to Run
1. Build and start the containers:
    ```sh
    docker compose up --build
    ```
2. Wait for the resources to load

## Clone the Repository
To clone the repository, run the following commands:
```sh
git clone https://github.com/juancmacias/Scrapy-Coin-Meme.git
cd Scrapy-Coin-Meme
```

## If the Repository Already Exists
If the repository already exists, you can add the remote and push the changes:
```sh
git remote add origin https://github.com/juancmacias/Scrapy-Coin-Meme.git
git branch -M main
git push -u origin main
```