from fastapi import FastAPI, Request, Form,  Response
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import pandas as pd
from datetime import datetime
from app.cadenas_ale import generar_cadena_aleatoria

import mongo.connect as mc
import app.write_log as wr
import app.archivo as arch

app_f = FastAPI()

app_f.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory = "templates")

@app_f.api_route("/data", methods=["GET", "POST"])
async def show_database(request: Request):
    try:
        dolar_price = mc.get_data_euro()
        wr.write_log(f"✅ Datos de dólar recuperados correctamente")
        return {"dolar_price": dolar_price}
    except Exception as e:
        wr.write_log(f"❌ Error al recuperar datos: {e}")
        print(f"❌ Error al recuperar datos: {e}")
        return {"dolar_price": []}



@app_f.get("/download")
def excel(request: Request):
    try:
        result, last_date, price_dolar = mc.obtener_coleccion("recoleccion", datetime.now())
        for item in result:
            precio = item["price"]
            precio_float = round(float(precio), 2)*round(float(price_dolar), 2)
            item["euro"] = round(precio_float, 2)
            
        df = pd.DataFrame(result)
    # Guardar en un archivo Excel
        archivo = f"/app/{generar_cadena_aleatoria()}.xlsx"
        df.to_excel(archivo, index=False)
        wr.write_log(f"📊 Archivo Excel generado: {archivo}")
    except Exception as e:
        print(f"❌ Error al recuperar algo {e}")
        wr.write_log(f"❌ Error al recuperar algo {e}")
    return FileResponse(archivo, filename=archivo, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")


# Endpoint para lanzar el scraping en un hilo separado

@app_f.get("/", response_class=HTMLResponse)
def show_database_all(request: Request):
    try:
        result, last_date, price_dolar = mc.obtener_coleccion("recoleccion", datetime.now())  # Obtener datos de MongoDB
        lectura = arch.leer_archivo()  # Leer archivo
        for item in result:
            precio = item["price"]
            precio_float = round(float(precio), 2)*round(float(price_dolar), 2)
            item["euro"] = round(precio_float, 2)
        wr.write_log(f"✅ Datos recuperados correctamente")
    except Exception as e:
        wr.write_log(f"❌ Error al recuperar datos {e}")
        print(f"❌ Error al recuperar algo {e}")
        result = []  # Devolver una lista vacía en caso de error
        lectura = ""
    return templates.TemplateResponse(request, "index.html", {
        "request": request,
        "lectura": lectura,
        "last_date": last_date.strftime("%d-%m-%Y %H:%M:%S"),
        "cryptos": result,
        "price_dolar": price_dolar
    })

if __name__ == "__main__":
    app_f.run(debug=True)