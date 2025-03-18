from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

def guardar_precio_dolar(fecha, precio):

    # mongodb
    uri = "mongodb+srv://juancarlos:mVcT29ErVz5uV2lV@cluster0.fkh7n.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'))
    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        db = client["ejercicio"]  # Nombre de la base de datos
        collection = db["precio_dolar"]  # Nombre de la colección

        print("Conexión exitosa a MongoDB")
        documento = {
            "date": fecha,
            "price": precio,
        }

        resultado = collection.insert_one(documento)
        #print("ID del documento insertado:", resultado.inserted_id)
    except Exception as e:
        print(e)
    finally:
            # Cerrar la conexión a MongoDB 
        if client:
            client.close()
            print("Conexión a MongoDB cerrada.")