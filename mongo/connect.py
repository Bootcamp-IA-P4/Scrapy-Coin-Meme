from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo.errors import ConnectionFailure
from pymongo.collection import Collection
import os
from fastapi import Query
import app_base.write_log as wr
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
load_dotenv()
MONGODB = os.getenv("MONGODB_URI")

def serialize_document(document):
    """Convierte ObjectId a string y datetime a ISO 8601 en documentos MongoDB."""
    document["_id"] = str(document["_id"])  # Convierte ObjectId a string
    document["date"] = document["date"].isoformat()  # Convierte datetime a string ISO 8601
    return document
# Connect to MongoDB
def obtener_conexion(conect):
    """Establece y devuelve una conexión a MongoDB."""
    try:
        client = MongoClient(MONGODB, serverSelectionTimeoutMS=5000)
        client.admin.command('ping')  # Verificar conexión
        print(f"✅ Conexión establecida a MongoDB Atlas: {conect}")
        wr.write_log(f"🚍 Conexión a MongoDB Atlas: {conect}")
        return client
    except ConnectionFailure as e:
        print(f"❌ connect.py/obtener_conexion Error de conexión: {e}")
        return None
# clean price
def limpiar_precio(precio):
    """Convierte el precio a float, eliminando caracteres innecesarios"""
    return float(precio.replace(" ", "").replace("US$", "").replace(".", "").replace(",", ".").strip())
# insert data dolar
def guardar_precio_dolar(fecha, precio):
    client = obtener_conexion("Insertar Dolar")
    #fecha = fecha.replace(tzinfo=timezone.utc).isoformat(timespec='seconds')

    try:
        db = client["ejercicio"]  # Nombre de la base de datos
        collection = db["precio_dolar"]  # Nombre de la colección
        documento = {
            "date":  fecha,
            "price": limpiar_precio(precio),
        }
        resultado = collection.insert_one(documento)
        #print("ID del documento insertado:", resultado.inserted_id

    except Exception as e:
        print(e)
    finally:
        client.close()
# insertar una nueva fecha
def save_date():
    client = obtener_conexion("Insertar fecha")
    ahora = datetime.now()
    ahora += timedelta(hours=1)
    
    try:
        db = client["ejercicio"]  # Nombre de la base de datos
        collection = db["fecha"]  # Nombre de la colección
        documento = {
            "date": ahora,
        }
        resultado = collection.insert_one(documento)
        print("ID del documento insertado:", resultado.inserted_id)
        wr.write_log(f"📅 Fecha insertada: {resultado.inserted_id}")
        return resultado.inserted_id
    except Exception as e:
        print(e)
    finally:
        client.close()


# insert data coin
# Inserta todas, a la ve'ceta, las criptomonedas en la base de datos
def save_coin_(fecha_actual, datos):
    id_fecha = save_date()
    client = obtener_conexion("Insertar monedas")
    print("<<<<----Fecha seleccionada:", len(datos["cryptos"]), id_fecha)
    wr.write_log(f"📅 insertados: {len(datos['cryptos'])}, {id_fecha}")
    try:
        
        db = client["ejercicio"]  # Nombre de la base de datos
        collection = db["recoleccion"]  # Nombre de la colección
        for doc in datos["cryptos"]:
            price = doc["price"]
            doc["date_id"] = id_fecha
            doc["price"] = limpiar_precio(price)
        collection.insert_many(datos["cryptos"])
        #resultado = collection.insert_one(documento)
        print("ID del documento insertado:",id_fecha)
    except Exception as e:
        print(e)
    finally:
        client.close()

# Show data
def obtener_coleccion(name_coleccion, date_first):
    """Recupera todos los documentos de una colección."""
    client = obtener_conexion("Recuperar colecciones")
    print("Recuperación:", name_coleccion, date_first)
    try:
        db = client["ejercicio"]  # Selecciona la base de datos
        collection_fecha = db["fecha"]  # Selecciona la colección de fechas
        ultimo_date = collection_fecha.find_one(sort=[("_id", -1)])  # Recupera el último documento por _id
        
        
        collection_datos = db[name_coleccion]  # Selecciona la colección de datos
        documentos = list(collection_datos.find({"date_id": ultimo_date["_id"]}))  # Recupera documentos con date_id igual al _id del último documento
        
        collection_precio_dolar = db["precio_dolar"]  # Selecciona la colección de precios del dólar
        ultimo_dolar = collection_precio_dolar.find_one(sort=[("_id", -1)])  # Recupera el último documento por _id
        print("<<<<----Precio seleccion", len(documentos), ultimo_date["_id"] , ultimo_dolar["price"], ultimo_dolar["date"], ultimo_dolar["_id"])
        return documentos, ultimo_date["date"], ultimo_dolar["price"]
    except Exception as e:
        print(f"❌ connect.py/obtener_coleccion Error al obtener colección: {e}, {name_coleccion}")
        wr.write_log(f"❌ Error al obtener colección: {e}, {name_coleccion}")
        return []
    finally:
        client.close()  # Cierra la conexión después de la operación

def get_data_euro(range: str = Query("day", enum=["day", "week", "month", "year"])):
    client = obtener_conexion("Recuperar euro")
    now = datetime.now(timezone.utc)
    start_date = now
    print(f"📅 Rango seleccionado: {range}")
    if range == "day":
        start_date -= timedelta(days=1)
    elif range == "week":
        start_date -= timedelta(weeks=1)
    elif range == "month":
        start_date -= timedelta(days=30)
    elif range == "year":
        start_date -= timedelta(days=365) 
     
    try:
        db = client["ejercicio"]  # Nombre de la base de datos
        collection = db["precio_dolar"]  # Nombre de la colección
        #start_date = start_date.replace(tzinfo=timezone.utc).isoformat(timespec='seconds')  
        #now = now.replace(tzinfo=timezone.utc).isoformat(timespec='seconds')   
        #start_date = datetime(start_date, tzinfo=timezone.utc)  # Fecha de inicio en UTC
        #now = datetime(now, tzinfo=timezone.utc)
        query = {"date": {"$gte": start_date, "$lte": now}}

        #print(f"📅 Fecha de inicio: {now}, Fecha final: {start_date}") 
         
        items = list(collection.find(query).sort("date", -1).limit(30))
        #print(f"✅ Datos de euro chart: {len(items)}")
        wr.write_log(f"📅 Periodo seleccionado: {range}")
        wr.write_log(f"📅 Fecha de inicio: {now}, Fecha final: {start_date}")
        wr.write_log(f"✅ Datos de euro chart: {len(items)}")
        return {"euro": [serialize_document(item) for item in items]}  # Serializa los documentos
    except Exception as e:
        wr.write_log(f"❌ connect.py/get_data_euro Error al obtener euro chart: {e}")
        print(f"❌ connect.py/get_data_euro Error al obtener euro chart: {e}")
        return []
    finally:
        client.close()  # Cierra la conexión después de la operación
    

## ---->
def get_collection(collection_name: str) -> Collection:
    client = obtener_conexion(collection_name)
    db = client["ejercicio"]
    return db[collection_name]

## para websocket
async def consultar_mongo():
    client = obtener_conexion("WebSocket")
    db = client["ejercicio"]
    collection_fecha = db["fecha"]  # Selecciona la colección de fechas
    ultimo_date = collection_fecha.find_one(sort=[("_id", -1)]) # Último registro
    if ultimo_date:
        return ultimo_date["date"]
    return "No hay nuevas notificaciones", datetime.utcnow()