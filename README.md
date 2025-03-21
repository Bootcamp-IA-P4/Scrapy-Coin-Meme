# Meme Coin Scraping
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
    - Limpiea de los datos sobre todo en los números
- ✅ Implementación de logs para trazabilidad del scraper.
- ❌ Tests unitarios para validar el funcionamiento del código.

### 🟠 Nivel Avanzado:
- ❌ Uso de Programación Orientada a Objetos (OOP) para mejorar la estructura del código.
- ✅ Manejo robusto de errores para evitar bloqueos y baneos de IP.
- ✅ Automatización del scraper para actualizar periódicamente la base de datos con tareas Cron.

### 🔴 Nivel Experto:
- ✅ Dockerización completa del proyecto para facilitar despliegue y escalabilidad.
- ✅ Implementación de un frontend interactivo para visualizar datos en tiempo real.
- ✅ Despliegue en un servidor accesible públicamente.
- ✅ Integración con múltiples sitios web de empleo para mejorar la cantidad y calidad de datos recopilados.

## Prerequisites
- Ensure Docker is running

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