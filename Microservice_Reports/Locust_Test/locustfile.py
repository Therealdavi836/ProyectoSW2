from locust import HttpUser, task, between
import random

class ReportServiceTest(HttpUser):
    wait_time = between(1, 3)
    
    # Reemplazar con un token válido del microservicio de autenticación
    token = "Bearer TOKEN"

    @task(2)
    def generate_pdf_report(self):
        """Simula la generación de un reporte PDF"""
        headers = {"Authorization": self.token}
        payload = {
            "ms_url": "http://127.0.0.1:8001/vehicles",  # Micro consultado
            "type": f"vehiculos_{random.randint(1, 100)}"
        }

        with self.client.post("/report/pdf", json=payload, headers=headers, catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            elif response.status_code == 500:
                response.failure("Error interno del servidor (PDF 500)")
            else:
                response.failure(f"Error inesperado PDF: {response.status_code}")

    @task(2)
    def generate_excel_report(self):
        """Simula la generación de un reporte Excel"""
        headers = {"Authorization": self.token}
        payload = {
            "ms_url": "http://127.0.0.1:8001/vehicles",
            "type": f"vehiculos_{random.randint(1, 100)}"
        }

        with self.client.post("/report/excel", json=payload, headers=headers, catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            elif response.status_code == 500:
                response.failure("Error interno del servidor (Excel 500)")
            else:
                response.failure(f"Error inesperado Excel: {response.status_code}")

    @task(1)
    def health_check(self):
        """Verifica el estado del microservicio"""
        with self.client.get("/report/health", catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Servicio no disponible ({response.status_code})")