
from datetime import datetime
import concurrent.futures
import scraping.scraper_coin as sc
import mongo.connect as mc
import app_base.write_log as wr

def scrape_coin():
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(sc.scrape_data)
        result = future.result()
        print("🚚 Esto es lo que devuelve", result)
        mc.save_coin_(datetime.now(), result)
        wr.write_log(f"Scrapig de cripto monedas total:{result['total']} terminado")

if __name__ == "__main__":
    wr.write_log("Init sc Coin")
    scrape_coin()