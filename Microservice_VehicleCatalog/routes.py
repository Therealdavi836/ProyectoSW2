# microservice_catalog/routes.py

from fastapi import APIRouter, HTTPException
from .models import Vehicle
from . import crud
import requests

router = APIRouter(prefix="/vehicles", tags=["Vehicles"])

# Función auxiliar para enviar notificaciones
def send_notification(user_id: int, title: str, message: str, type_: str):
    """
    Envía una notificación al microservicio de notificaciones.
    Si el servicio no está disponible, simplemente ignora el error.
    """
    try:
        requests.post(
            "http://127.0.0.1:8003/api/notifications/",
            json={
                "user_id": user_id,
                "title": title,
                "message": message,
                "type": type_,
            },
            timeout=3  # Evita que se bloquee el flujo si el servicio no responde
        )
    except requests.exceptions.RequestException:
        # Silencia el error si el servicio de notificaciones falla
        pass

# Endpoints del microservicio de Catálogo de Vehículos

# Crear un nuevo vehículo
@router.post("/")
async def create_vehicle(vehicle: Vehicle):
    id = await crud.create_vehicle(vehicle)

    # Enviar notificación
    send_notification(
        user_id=1,
        title="Nuevo vehículo agregado",
        message=f"El vehículo {vehicle.brand} {vehicle.model} ha sido añadido al catálogo.",
        type_="info"
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
async def update_vehicle(id: str, vehicle: Vehicle):
    updated_vehicle = await crud.update_vehicle(id, vehicle.dict())
    if not updated_vehicle:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")

    # Enviar notificación
    send_notification(
        user_id=1,
        title="Vehículo modificado",
        message=f"El vehículo {vehicle.brand} {vehicle.model} ha sido modificado.",
        type_="info"
    )

    return updated_vehicle


# Eliminar un vehículo
@router.delete("/{id}")
async def delete_vehicle(id: str):
    result = await crud.delete_vehicle(id)
    if not result:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")

    # Enviar notificación
    send_notification(
        user_id=1,
        title="Vehículo eliminado",
        message=f"Un vehículo del catálogo ha sido eliminado.",
        type_="warning"
    )

    return {"message": "Vehículo eliminado correctamente"}