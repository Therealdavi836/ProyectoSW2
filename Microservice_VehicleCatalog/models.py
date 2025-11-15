from pydantic import BaseModel
from typing import Optional

class Vehicle(BaseModel):
    brand: str
    model: str
    year: int
    price: float
    category: str
    motor_type: str
    mileage: float

class VehicleResponse(Vehicle):
    id: str