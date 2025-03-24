import asyncio
import random
from datetime import datetime, timedelta
from fastapi import WebSocket
from mongo.connect import consultar_mongo   # Importa la conexión a MongoDB

async def enviar_actualizaciones(websocket: WebSocket):
    # Notificacion 
    await websocket.accept()
    while True:
        await asyncio.sleep(30)  # Espera 60 segundos
        fecha = await consultar_mongo()
        now = datetime.utcnow()
        now = now + timedelta(hours=1)
        tiempo_transcurrido = now - fecha
        
        mensaje = {"nueva_info": True, "mensaje": f"¡Nuevos cambios! hace: {tiempo_transcurrido.seconds // 60} min"}
        await websocket.send_json(mensaje)

async def websocket_endpoint(websocket: WebSocket):
    # Endpoint WebSocket que llama a enviar_actualizaciones()
    await enviar_actualizaciones(websocket)