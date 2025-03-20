from fastapi import FastAPI, Request, Form,  Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from datetime import datetime
from itertools import groupby
import mongo.connect as mc

import app.archivo as arch

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory = "templates")




# Endpoint para lanzar el scraping en un hilo separado
@app.get("/", response_class=HTMLResponse)
def show_database_all(request: Request):
    try:
        result = mc.obtener_coleccion("recoleccion", datetime.now())  # Obtener datos de MongoDB
        lectura = arch.leer_archivo()  # Leer archivo
    except Exception as e:
        print(f"❌ Error al recuperar {e}")
        result = []  # Devolver una lista vacía en caso de error
        lectura = ""

    
    return templates.TemplateResponse(request, "index.html", {
        "request": request,
        "lectura": lectura,
        "cryptos": result,
    })