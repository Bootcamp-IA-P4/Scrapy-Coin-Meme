
from datetime import datetime
import dolar as dl
import mongo.connect as mc
import app.write_log as wr

def scrape_dolar():
    precio = dl.get_dolar()
    mc.guardar_precio_dolar(datetime.now(), precio)
    wr.write_log("Scraping Dolar finalizado")

if __name__ == "__main__":
    wr.write_log("Init sc Dolar")
    scrape_dolar()