from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo.errors import ConnectionFailure
import os
import app.write_log as wr
from datetime import datetime, timedelta

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
    client = obtener_conexion("Dolar")
    try:
        db = client["ejercicio"]  # Nombre de la base de datos
        collection = db["precio_dolar"]  # Nombre de la colección
        documento = {
            "date": fecha,
            "price": precio,
        }
        resultado = collection.insert_one(documento)
        #print("ID del documento insertado:", resultado.inserted_id

    except Exception as e:
        print(e)
    finally:
        client.close()
# insertar una nueva fecha
def save_date():
    client = obtener_conexion("Fecha")
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
def save_coin_(fecha_actual, datos):
    id_fecha = save_date()
    client = obtener_conexion("Monedas")
    try:
        
        db = client["ejercicio"]  # Nombre de la base de datos
        collection = db["recoleccion"]  # Nombre de la colección
        for doc in datos["cryptos"]:
            doc["date_id"] = id_fecha
            doc["price"] = limpiar_precio(doc["price"])
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
    client = obtener_conexion("Recuperar")
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
