#Practicas de pruebas de software 
#ejemplo de concurrencia de productos

#Import 
from locust import HttpUser, task

# clase usuario que usa un ejemplo de HttpUser como instancia 
class SimpleUser(HttpUser):
    """
    Testeamos los metodos de CRUD con una api super simple 
    """
    #hacemos test del metodo Get
    @task
    def get_product(self):
        self.client.get("/")
    
    #hacemos test del metodo post
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

    #hacemos test del metodo put
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

    #hacemos test del metodo Delete
    @task
    def delete_product(self):
        self.client.delete("/1")