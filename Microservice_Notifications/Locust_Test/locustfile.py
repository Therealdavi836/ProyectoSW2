from locust import HttpUser, task, between

class NotificationLoadTest(HttpUser):
    wait_time = between(1, 3)  # Simula pausas humanas entre peticiones

    @task(3)
    def crear_notificacion(self):
        """Prueba el endpoint POST /api/notifications/"""
        payload = {
            "user_id": 1,
            "title": "Prueba de carga",
            "message": "Notificación de prueba bajo carga",
            "type": "info"
        }
        headers = {"Content-Type": "application/json"}
        self.client.post("/api/notifications/", json=payload, headers=headers)