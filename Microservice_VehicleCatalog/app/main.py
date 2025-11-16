from fastapi import FastAPI
from app.routes import router as vehicle_router

app = FastAPI(title="Microservicio de Catálogo de Vehículos", version="1.0")

app.include_router(vehicle_router)