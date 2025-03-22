from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#from selenium.webdriver.chrome.options import Options
#from selenium.webdriver.chrome.service import Service
# firefox
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
import concurrent.futures
import app_base.write_log as wr
import time
import os



# Configurar Selenium con Chrome en modo headless
def get_driver():
    wr.write_log("✅ Init get_driver")
    options = Options()
    #options = webdriver.ChromeOptions()
    #options.binary_location = os.getenv("CHROMIUM_PATH", ) # Ruta de Chrome en Heroku
    options.add_argument("--headless")  # Ejecutar sin interfaz gráfica
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    #service = Service(ChromeDriverManager().install())
    service = Service(os.getenv("CHROMEDRIVER_PATH")) # Ruta de ChromeDriver en Heroku
    return webdriver.Firefox(service=service, options=options)


# Función para hacer scroll gradualmente y esperar la carga
def scroll_and_wait(driver):
    wr.write_log("✅ Init scroll_and_wait")
    last_count = 0
    retries = 5  # Número máximo de intentos antes de detenernos

    while retries > 0:
        rows = driver.find_elements(By.CSS_SELECTOR, "tr")
        new_count = len(rows)

        if new_count > last_count:
            retries = 5  # Reiniciar intentos si encontramos nuevos elementos
        else:
            retries -= 1  # Reducir intentos si no encontramos más

        last_count = new_count

        driver.execute_script("window.scrollBy(0, 2000);")  # Scroll suave
        time.sleep(1.5)  # Esperar a que se carguen nuevos elementos

# Función para extraer datos de una fila
def extract_row_data(row):
    wr.write_log("✅ Init extract_row_data")
    try:
        script = """
        let row = arguments[0];
        return {
            rank: row.querySelector("p.jBOvmG")?.innerText || '',
            name: row.querySelector("p.iPbTJf")?.innerText || '',
            price: row.querySelector("div.lmjbLF span")?.innerText || '',
            market_cap: row.querySelector("span.chpohi")?.innerText || '',
            volume: row.querySelector("a.cmc-link p.bbHOdE")?.innerText || '',
            supply: row.querySelector("div.circulating-supply-value span")?.innerText || '',
            image_url: row.querySelector("img.coin-logo")?.src || ''
        };
        """
        return row.parent.execute_script(script, row)
    except Exception as e:
        print(f"❌ scraper_cron.py Error obtención scraping: {e}")
        return {"error": str(e)}

# Función principal de scraping
def scrape_data():
    wr.write_log("✅ Init scrape_data on coinmarketcap.com")
    driver = get_driver()
    #driver.get("https://coinmarketcap.com/es/view/memes/")
    driver.get("https://coinmarketcap.com/es/")
    
    try:
        # Esperar a que la tabla aparezca
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "tr"))
        )

        # Hacer scroll suave para cargar todos los datos
        scroll_and_wait(driver)

        # Extraer filas después de hacer scroll
        rows = driver.find_elements(By.CSS_SELECTOR, "tr")[1:]  # Omitir encabezado
        total_elements = len(rows)
        cryptos = []

        # Usar hilos para extraer datos más rápido
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            results = list(executor.map(extract_row_data, rows))

        cryptos.extend(results)

        return {"total": total_elements, "cryptos": cryptos}

    except Exception as e:
        print(f"❌ scraper_cron.py Error on init scraping: {e}")
        return {"error": str(e)}

    finally:
        wr.write_log("Closing driver")
        driver.quit()