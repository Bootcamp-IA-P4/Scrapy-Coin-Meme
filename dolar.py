import sys
import os
import time
import re
# Agregar la ruta del proyecto al PYTHONPATH

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
#from selenium.webdriver.chrome.service import Service
#from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
import app.write_log as wr


def get_dolar():
    # Configurar opciones de Chrome para modo headless (sin abrir ventana)
    opciones = Options()
    #opciones.binary_location = os.getenv("CHROMIUM_PATH", )
    opciones.add_argument("--headless")
    opciones.add_argument("--no-sandbox")
    opciones.add_argument("--disable-dev-shm-usage")

    # Iniciar el driver en este caso GeckoDriver
    service = Service(os.getenv("CHROMEDRIVER_PATH"))
    driver = webdriver.Firefox(service=service, options=opciones)

    try:
        # URL de la página a scrapear
        #url = "https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/eurofxref-graph-usd.es.html"
        url = "https://www.xe.com/es/currencyconverter/convert/?Amount=1&From=USD&To=EUR"
        driver.get(url)
        
        # Esperar a que cargue el elemento y obtener el precio
        #precio = driver.find_element(By.CSS_SELECTOR, ".embed-rate.span").text
         # Esperar hasta que el precio esté visible (máximo 10 segundos)
        wait = WebDriverWait(driver, 5)
        time.sleep(3)
        precio = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".sc-294d8168-1"))).text
        precio = precio.replace(" Euros", "")
        precio = precio.replace(",", ".").strip()
        wr.write_log(f"Dolar:  {precio}")
        return precio
    except Exception as e:
        return (f"Error: {e}")
    
    finally:
        driver.quit()