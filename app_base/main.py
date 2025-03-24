import os
from fastapi import FastAPI, Request, Form,  Response, Query, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
import app_base.auth.auth
import pandas as pd
from datetime import datetime
from app_base.cadenas_ale import generar_cadena_aleatoria

import mongo.connect as mc
import app_base.write_log as wr
import app_base.archivo as arch

app = FastAPI(
    title="Scraping de Criptomonedas & autenticación",
    description="A FastAPI-based authentication system connected to MongoDB",
    version="1.0.0"
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory = "templates")

# LOGIN ---
# Add session middleware
app.add_middleware(
    SessionMiddleware, 
    secret_key=os.environ.get("SESSION_SECRET", "supersecretkey")
)

# Setup OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Include auth router
app.include_router(app_base.auth.auth.router)
@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/protected")
async def protected_route(token: str = Depends(oauth2_scheme)):
    """
    Protected route that requires authentication
    """
    credentials = app_base.auth.verify_token(token)
    if not credentials:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"message": f"Hello, {credentials['username']}! This is a protected route."}

# LOGIN ---
@app.api_route("/data", methods=["GET", "POST"])
async def show_database(range: str = Query("day", enum=["day", "week", "month", "year"])):
    try:
        dolar_price = mc.get_data_euro(range)
        wr.write_log(f"✅ Datos de dólar recuperados correctamente")
        #print("seleccionado", dolar_price)  
        return dolar_price
    except Exception as e:
        wr.write_log(f"❌ Error al recuperar datos: {e}")
        print(f"❌ Error al recuperar datos: {e}")
        return {"dolar_price": []}



@app.get("/download")
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

@app.get("/", response_class=HTMLResponse)
def show_database_all(request: Request):
    try:
        result, last_date, price_dolar = mc.obtener_coleccion("recoleccion", datetime.now())  # Obtener datos de MongoDB
        lectura = arch.leer_archivo()  # Leer archivo
        for item in result:
            precio = item["price"]
            precio_float = round(float(precio), 2)*round(float(price_dolar), 2)
            item["euro"] = round(precio_float, 2)
        wr.write_log(f"✅ Datos recuperados correctamente")
        #date_obj = datetime.fromisoformat(last_date)
    except Exception as e:
        wr.write_log(f"❌ Error al recuperar datos {e}")
        print(f"❌ Error al recuperar algo {e}")
        result = []  # Devolver una lista vacía en caso de error
        lectura = ""
    return templates.TemplateResponse(request, "index.html", {
        "request": request,
        "lectura": lectura,
        "last_date": last_date,
        "cryptos": result,
        "price_dolar": price_dolar
    })

if __name__ == "__main__":
    app.run(debug=True)