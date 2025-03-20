from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo.errors import ConnectionFailure
import os
import app.write_log as wr

MONGODB = "mongodb+srv://juancarlos:mVcT29ErVz5uV2lV@cluster0.fkh7n.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
def obtener_conexion(conect):
    """Establece y devuelve una conexión a MongoDB."""
    try:
        client = MongoClient(MONGODB, serverSelectionTimeoutMS=5000)
        client.admin.command('ping')  # Verificar conexión
        print(f"✅ Conexión establecida a MongoDB Atlas: {conect}")
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
# insert data coin
def save_coin_(fecha_actual, datos):
    client = obtener_conexion("Monedas")
    try:
        
        db = client["ejercicio"]  # Nombre de la base de datos
        collection = db["recoleccion"]  # Nombre de la colección
        for doc in datos["cryptos"]:
            doc["date"] = fecha_actual
        collection.insert_many(datos["cryptos"])
        #resultado = collection.insert_one(documento)
        #print("ID del documento insertado:", resultado.inserted_id)
    except Exception as e:
        print(e)
    finally:
        client.close()

# Show data
def obtener_coleccion(name_coleccion, date_first):
    """Recupera todos los documentos de una colección."""
    client = obtener_conexion("Recuperar")
    print("Recuperación:", name_coleccion, date_first)
    query = {
        "fecha": {
            "$gte": date_first + date_first.timedelta(minutes=-10),  # Mayor o igual a hace 10 minutos
            "$lte": date_first  # Menor o igual a ahora
        }
    }
    print("fechas ", date_first, date_first + date_first.timedelta(minutes=-10))
    try:
        db = client["ejercicio"]  # Selecciona la base de datos
        collection = db[name_coleccion]  # Selecciona la colección

        documentos = list(collection.find(query))  # Recuperar sin _id
        return documentos
    except Exception as e:
        print(f"❌ Error al obtener colección: {e}, {name_coleccion}")
        return []
    finally:
        client.close()  # Cierra la conexión después de la operación
