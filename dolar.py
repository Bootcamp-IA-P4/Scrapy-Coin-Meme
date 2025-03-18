import sys
import os

# Agregar la ruta del proyecto al PYTHONPATH
sys.path.append("/app")
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def price_dolar():
    # Configurar opciones de Chrome para modo headless (sin abrir ventana)
    opciones = Options()
    opciones.binary_location = os.getenv("CHROMIUM_PATH", )
    opciones.add_argument("--headless")
    opciones.add_argument("--disable-gpu")
    opciones.add_argument("--no-sandbox")

    # Iniciar el driver
    service = Service(os.getenv("CHROMEDRIVER_PATH"))
    driver = webdriver.Chrome(service=service, options=opciones)

    try:
        # URL de la página a scrapear
        url = "https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/eurofxref-graph-usd.es.html"
        driver.get(url)

        # Esperar a que cargue el elemento y obtener el precio
        #precio = driver.find_element(By.CSS_SELECTOR, ".embed-rate.span").text
         # Esperar hasta que el precio esté visible (máximo 10 segundos)
        wait = WebDriverWait(driver, 15)
        precio = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".embed-rate span"))).text

        return precio
        #print(f"Precio actual de Bitcoin: {precio}")

    except Exception as e:
        return (f"Error: {e}")
    
    finally:
        driver.quit()