import sys
import os
import json
# Agregar la ruta del proyecto al PYTHONPATH
#sys.path.append("/app")
#import requests
#import requests
#from requests import Response
from datetime import datetime
import dolar as dl
#import mongo.connect as mc
#import httpx
#from selectolax.parser import HTMLParser


def scrape():
    precio = dl.get_dolar()
    write_log(f"Precio del dolar: {precio}")

def write_log(text):
    with open("/app/log.txt", "a") as log:
        log.write(f"[{datetime.now()}] {text}\n")

if __name__ == "__main__":
    write_log("Iniciando scraping")
    scrape()