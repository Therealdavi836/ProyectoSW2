#Practicas de pruebas de software 
#ejemplo de concurrencia de productos

#Import 
from locust import HttpUser, task

class SimpleUser(HttpUser):
    @task
    def get_product(self):
        self.client.get("/")
    
    @task
    def create_product(self):
        data = {
            "title": "Producto nuevo",
            "price": 20.1,
            "description": "ejemplo de creacion de productos",
            "category": "electronic",
            "image": "http://example.com"
        }
        self.client.post("/", json=data)

    @task
    def update_product(self):
        data = {
            "id": 0,
            "title": "Producto nuevo",
            "price": 20.1,
            "description": "ejemplo de creacion de productos",
            "category": "electronic",
            "image": "http://example.com"
        }
        self.client.put("/1", json=data)

    @task
    def delete_product(self):
        self.client.delete("/1")