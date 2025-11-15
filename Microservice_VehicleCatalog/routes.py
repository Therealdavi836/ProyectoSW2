# microservice_catalog/routes.py

from fastapi import APIRouter, HTTPException, Request
from .models import Vehicle
from . import crud
import requests

router = APIRouter(prefix="/vehicles", tags=["Vehicles"])

# URL del Gateway para reenviar notificaciones
GATEWAY_URL = "http://127.0.0.1:8000/api/forward/notifications/"

# Función auxiliar para enviar notificaciones a través del Gateway
def send_notification(user_id: int, title: str, message: str, type_: str, token: str):
    """
    Envía una notificación al microservicio de notificaciones a través del Gateway.
    Usa el token que se recibe dinámicamente.
    """
    try:
        requests.post(
            GATEWAY_URL,
            headers={
                "Authorization": token,  # token dinámico recibido desde el request
                "Accept": "application/json"
            },
            json={
                "user_id": user_id,
                "title": title,
                "message": message,
                "type": type_
            },
            timeout=3
        )
    except requests.exceptions.RequestException:
        pass  # Silencia errores de comunicación


# ==========================
# Endpoints de Vehicles
# ==========================

# Crear un nuevo vehículo
@router.post("/")
async def create_vehicle(vehicle: Vehicle, request: Request):
    id = await crud.create_vehicle(vehicle)

    token = request.headers.get("Authorization", "")
    send_notification(
        user_id=1,
        title="Nuevo vehículo agregado",
        message=f"El vehículo {vehicle.brand} {vehicle.model} ha sido añadido al catálogo.",
        type_="info",
        token=token
    )

    return {"id": id}


# Obtener todos los vehículos
@router.get("/")
async def get_vehicles():
    return await crud.get_vehicles()


# Obtener un vehículo por ID
@router.get("/{id}")
async def get_vehicle(id: str):
    vehicle = await crud.get_vehicle(id)
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")
    return vehicle


# Actualizar un vehículo
@router.put("/{id}")
async def update_vehicle(id: str, vehicle: Vehicle, request: Request):
    updated_vehicle = await crud.update_vehicle(id, vehicle.dict())
    if not updated_vehicle:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")

    token = request.headers.get("Authorization", "")
    send_notification(
        user_id=1,
        title="Vehículo modificado",
        message=f"El vehículo {vehicle.brand} {vehicle.model} ha sido modificado.",
        type_="info",
        token=token
    )

    return updated_vehicle


# Eliminar un vehículo
@router.delete("/{id}")
async def delete_vehicle(id: str, request: Request):
    result = await crud.delete_vehicle(id)
    if not result:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")

    token = request.headers.get("Authorization", "")
    send_notification(
        user_id=1,
        title="Vehículo eliminado",
        message="Un vehículo del catálogo ha sido eliminado.",
        type_="warning",
        token=token
    )

    return {"message": "Vehículo eliminado correctamente"}