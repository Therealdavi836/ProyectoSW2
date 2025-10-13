#Creación del CRUD para el microservicio de catálogo de vehículos

#Importamos la base de datos y el modelo de datos
from .database import vehiculos_collection
from .models import Vehicle
from bson import ObjectId

#Función para serializar los datos de los vehículos
def vehicle_serializer(vehicle) -> dict:
    return {
        "id": str(vehicle["_id"]),
        "brand": vehicle["brand"],
        "model": vehicle["model"],
        "year": vehicle["year"],
        "price": vehicle["price"],
        "category": vehicle["category"],
        "motor_type": vehicle["motor_type"],
        "mileage": vehicle["mileage"]
    }

#POST: Función para crear un nuevo vehículo
async def create_vehicle(data: Vehicle):
    vehicle = await vehiculos_collection.insert_one(data.dict())
    return str(vehicle.inserted_id)

#GET: Función para obtener todos los vehículos
async def get_vehicles():
    vehicles = []
    async for vehicle in vehiculos_collection.find():
        vehicles.append(vehicle_serializer(vehicle))
    return vehicles

#GET: Función para obtener un vehículo por su ID
async def get_vehicle(id: str):
    vehicle = await vehiculos_collection.find_one({"_id": ObjectId(id)})
    if vehicle:
        return vehicle_serializer(vehicle)
    return None

#PUT: Función para actualizar un vehículo por su ID
async def update_vehicle(id: str, data: Vehicle):
    await vehiculos_collection.update_one({"_id": ObjectId(id)}, {"$set": data})
    return await get_vehicle(id)

#DELETE: Función para eliminar un vehículo por su ID
async def delete_vehicle(id: str):
    await vehiculos_collection.delete_one({"_id": ObjectId(id)})
    return True