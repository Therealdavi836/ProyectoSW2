from locust import HttpUser, task, between
import random

def random_vehicle():
    """Genera datos aleatorios para crear o actualizar vehículos"""
    return {
        "brand": random.choice(["Toyota", "Mazda", "Chevrolet", "Ford", "Nissan"]),
        "model": f"{random.choice(['A','B','C'])}{random.randint(100,999)}",
        "year": random.randint(2010, 2025),
        "price": random.randint(30000000, 800000000),
        "category": random.choice(["Sedán", "SUV", "Hatchback", "Compacto"]),
        "motor_type": random.choice(["Gasoline", "Extra"]),
        "mileage": random.randint(0, 120000)
    }

class CatalogoVehiculosTest(HttpUser):
    wait_time = between(1, 2)
    vehicle_ids = []

    # --- POST ---
    @task
    def crear_vehiculo(self):
        """POST /vehicles — Crear vehículo"""
        vehicle = random_vehicle()
        with self.client.post("/vehicles", json=vehicle, name="/vehicles", catch_response=True) as resp:
            if resp.status_code in [200, 201]:
                try:
                    data = resp.json()
                    vid = data.get("id") or data.get("_id")
                    if vid:
                        self.vehicle_ids.append(vid)
                    resp.success()
                except:
                    resp.failure("Respuesta inválida del POST")
            else:
                resp.failure(f"Error POST: {resp.status_code}")

    # --- GET todos ---
    @task
    def obtener_todos(self):
        """GET /vehicles — Obtener todos"""
        with self.client.get("/vehicles", name="/vehicles", catch_response=True) as resp:
            if resp.status_code == 200:
                resp.success()
            else:
                resp.failure(f"Error GET todos: {resp.status_code}")

    # --- GET por ID ---
    @task
    def obtener_por_id(self):
        """GET /vehicles/{id} — Obtener vehículo"""
        if not self.vehicle_ids:
            return
        vid = random.choice(self.vehicle_ids)
        with self.client.get(f"/vehicles/{vid}", name="/vehicles/{id}", catch_response=True) as resp:
            if resp.status_code == 200:
                resp.success()
            else:
                resp.failure(f"Error GET ID {vid}: {resp.status_code}")

    # --- PUT ---
    @task
    def actualizar(self):
        """PUT /vehicles/{id} — Actualizar vehículo"""
        if not self.vehicle_ids:
            return
        vid = random.choice(self.vehicle_ids)

        # Genera nuevos datos válidos
        nuevos_datos = random_vehicle()

        with self.client.put(
            f"/vehicles/{vid}",
            json=nuevos_datos,
            name="/vehicles/{id}",
            catch_response=True
        ) as resp:
            if resp.status_code in [200, 204]:
                resp.success()
            else:
                resp.failure(f"Error PUT {vid}: {resp.status_code}")

    # --- DELETE ---
    @task
    def eliminar(self):
        """DELETE /vehicles/{id} — Eliminar vehículo"""
        if not self.vehicle_ids:
            return
        vid = random.choice(self.vehicle_ids)
        with self.client.delete(f"/vehicles/{vid}", name="/vehicles/{id}", catch_response=True) as resp:
            if resp.status_code == 200:
                try:
                    self.vehicle_ids.remove(vid)
                except ValueError:
                    pass
                resp.success()
            else:
                resp.failure(f"Error DELETE {vid}: {resp.status_code}")