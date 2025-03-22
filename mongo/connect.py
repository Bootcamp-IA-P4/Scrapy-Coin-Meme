from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo.errors import ConnectionFailure
import os
import app_base.write_log as wr
from datetime import datetime, timedelta
from dotenv import load_dotenv
load_dotenv()
MONGODB = os.getenv("MONGODB_URI")
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
        print(f"❌ Error de conexión: {e}")
        return None
# insert data dolar
def guardar_precio_dolar(fecha, precio):
    client = obtener_conexion("Insertar Dolar")
    try:
        db = client["ejercicio"]  # Nombre de la base de datos
        collection = db["precio_dolar"]  # Nombre de la colección
        documento = {
            "date": fecha,
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
    date_ok = ahora + timedelta(hours=1)
    try:
        db = client["ejercicio"]  # Nombre de la base de datos
        collection = db["fecha"]  # Nombre de la colección
        documento = {
            "date": date_ok,
        }
        resultado = collection.insert_one(documento)
        print("ID del documento insertado:", resultado.inserted_id)
        wr.write_log(f"📅 Fecha insertada: {resultado.inserted_id}")
        return resultado.inserted_id
    except Exception as e:
        print(e)
    finally:
        client.close()
# clean price
def limpiar_precio(precio):
    """Convierte el precio a float, eliminando caracteres innecesarios"""
    return float(precio.replace("US$", "").replace(".", "").replace(",", ".").strip())

# insert data coin
# Inserta todas, a la ve'ceta, las criptomonedas en la base de datos
def save_coin_(fecha_actual, datos):
    id_fecha = save_date()
    client = obtener_conexion("Insertar monedas")
    try:
        
        db = client["ejercicio"]  # Nombre de la base de datos
        collection = db["recoleccion"]  # Nombre de la colección
        for doc in datos["cryptos"]:
            doc["date_id"] = id_fecha
            doc["price"] = float(doc["price"].replace(",","."))
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
        collection = db["fecha"]  # Selecciona la colección
        ultimo_date = collection.find_one(sort=[("_id", -1)])  # Recupera el último documento por _id
        print(ultimo_date)
        collection = db[name_coleccion]  # Selecciona la colección
        documentos = list(collection.find({"date_id": ultimo_date["_id"]}))  # Recuperar documentos con date_id igual al _id del último documento
        collection = db["precio_dolar"]  # Selecciona la colección
        ultimo_dolar = collection.find_one(sort=[("_id", -1)])  # Recupera el último documento por _id
        return documentos, ultimo_date["date"], ultimo_dolar["price"]
    except Exception as e:
        print(f"❌ Error al obtener colección: {e}, {name_coleccion}")
        wr.write_log(f"❌ Error al obtener colección: {e}, {name_coleccion}")
        return []
    finally:
        client.close()  # Cierra la conexión después de la operación

def get_data_euro():
    client = obtener_conexion("Recuperar dolar")
    try:
        db = client["ejercicio"]  # Nombre de la base de datos
        collection = db["precio_euro"]  # Nombre de la colección
        documentos = collection.find() # Recupera todos los documentos de la colección
        print(f"✅ Datos de euro chart: {len(documentos)}")
        wr.write_log(f"✅ Datos de euro chart: {len(documentos)}")
        return documentos
    except Exception as e:
        print(f"❌ Error al obtener euro chart: {e}")
        return []
    finally:
        client.close()  # Cierra la conexión después de la operación