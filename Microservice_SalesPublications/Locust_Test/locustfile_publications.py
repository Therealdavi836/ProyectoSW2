from locust import HttpUser, task, between
import random, requests

class PublicationLoadTest(HttpUser):
    wait_time = between(1, 2)

    def on_start(self):
        # Ajustar este token por uno real de un usuario con role = seller
        self.token = "2005|D38n5ddP4dwHv64zl5mVfoYLnjI482JeTEvEyz7s5dabcc2d"
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        self.created_ids = []
        self.vehicle_ids = self._preload_vehicles()

    def _preload_vehicles(self):
        """Obtiene IDs válidos desde el microservicio de Catálogo"""
        try:
            res = requests.get("http://localhost:8001/vehicles")
            if res.status_code == 200:
                data = res.json()
                return [v["id"] for v in data[:10]]  # toma solo los primeros 10
        except Exception:
            pass
        return []

    # --- GET publicaciones ---
    @task(3)
    def listar_publicaciones(self):
        with self.client.get("/api/publications", headers=self.headers, name="/publications", catch_response=True) as r:
            if r.status_code == 200:
                r.success()
            else:
                r.failure(f"Error GET publicaciones: {r.status_code}")

    # --- POST nueva publicación ---
    @task(2)
    def crear_publicacion(self):
        if not self.vehicle_ids:
            return
        data = {
            "vehicle_id": random.choice(self.vehicle_ids),
            "title": f"Auto de prueba {random.randint(1,9999)}",
            "description": "Vehículo en excelente estado",
            "price": random.randint(30000, 150000)
        }
        with self.client.post("/api/publications", json=data, headers=self.headers, name="/publications", catch_response=True) as r:
            if r.status_code == 201:
                try:
                    pub = r.json()
                    self.created_ids.append(pub["id"])
                    r.success()
                except:
                    r.failure("Respuesta inválida del POST")
            else:
                r.failure(f"Error POST {r.status_code}")

    # --- GET por id ---
    @task(1)
    def ver_publicacion(self):
        if not self.created_ids:
            return
        pub_id = random.choice(self.created_ids)
        with self.client.get(f"/api/publications/{pub_id}", headers=self.headers, name="/publications/{id}", catch_response=True) as r:
            if r.status_code == 200:
                r.success()
            else:
                r.failure(f"Error GET id {pub_id}: {r.status_code}")

    # --- PUT actualización ---
    @task(1)
    def actualizar_publicacion(self):
        if not self.created_ids:
            return
        pub_id = random.choice(self.created_ids)
        update_data = {
            "title": "Título actualizado",
            "description": "Descripción modificada",
            "price": random.randint(40000, 180000)
        }
        with self.client.put(f"/api/publications/{pub_id}", json=update_data, headers=self.headers, name="/publications/{id}", catch_response=True) as r:
            if r.status_code == 200:
                r.success()
            else:
                r.failure(f"Error PUT {r.status_code}")

    # --- PATCH cambiar estado ---
    @task(1)
    def cambiar_estado(self):
        if not self.created_ids:
            return
        pub_id = random.choice(self.created_ids)
        new_status = random.choice(["activo", "inactivo", "vendido"])
        with self.client.patch(f"/api/publications/{pub_id}/status", json={"status": new_status}, headers=self.headers, name="/publications/{id}/status", catch_response=True) as r:
            if r.status_code == 200:
                r.success()
            else:
                r.failure(f"Error PATCH {r.status_code}")

    # --- DELETE publicación ---
    @task(1)
    def eliminar_publicacion(self):
        if not self.created_ids:
            return
        pub_id = self.created_ids.pop()
        with self.client.delete(f"/api/publications/{pub_id}", headers=self.headers, name="/publications/{id}", catch_response=True) as r:
            if r.status_code == 200:
                r.success()
            else:
                r.failure(f"Error DELETE {r.status_code}")
