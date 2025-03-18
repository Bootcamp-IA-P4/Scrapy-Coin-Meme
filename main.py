from fastapi import FastAPI, Request, Form,  Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import concurrent.futures
import scraper_cron as sc
import dolar as dl
import app.archivo as arch

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory = "templates")




# Endpoint para lanzar el scraping en un hilo separado
@app.get("/", response_class=HTMLResponse)
def show_database_all(request: Request):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(sc.scrape_data)
        result = future.result()
        #print(result)
    return templates.TemplateResponse(request, "index.html", {
        "request": request,
        "lectura": arch.leer_archivo(),
        "cryptos": result,
        
    })