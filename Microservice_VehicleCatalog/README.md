# Microservice Vehicle Catalog – Concesionario de Vehículos

Este microservicio permite la **gestión y administración del catálogo de vehículos** dentro del ecosistema de microservicios del concesionario de vehículos.  
Está desarrollado en **Python 3.13.3** utilizando **FastAPI** como framework principal y **MongoDB** como base de datos NoSQL.  
Proporciona las operaciones CRUD básicas (crear, leer, actualizar y eliminar vehículos) y sirve como fuente de datos para los microservicios de **Reportes**, **Publicaciones** y **Ventas**.  

---

### Tecnologías y dependencias principales

- **Lenguaje:** Python 3.13.3  
- **Framework:** FastAPI v0.118.0  
- **Base de datos:** MongoDB  
- **Driver asíncrono:** Motor  
- **Servidor:** Uvicorn  

#### Dependencias principales

```txt
bson
pymongo
fastapi
uvicorn
motor
pydantic
typing
requests
````

Instalación de dependencias:

```bash
pip install -r requirements.txt
```

---

### Configuración de la base de datos

El microservicio utiliza **MongoDB** como sistema de almacenamiento.
Se requiere crear una base de datos llamada `Catalog` y una colección `Vehicles` en **MongoDB Compass** o **Mongo Shell**.

```python
import motor.motor_asyncio

MONGO_URL = "mongodb://localhost:27017"
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)
db = client["Catalog"]
vehiculos_collection = db["Vehicles"]
```

* **Puerto por defecto:** `8001`
* **No requiere variables de entorno adicionales**
* **No tiene configuración especial (CORS, tiempo de espera, etc.)**

---

### Endpoints disponibles

#### 1. `POST /vehicles`

**Descripción:** Crea un nuevo vehículo en la base de datos.
**Ejemplo de cuerpo (JSON):**

```json
{
  "brand": "Ford",
  "model": "Explorer",
  "year": 2022,
  "price": 245000000,
  "category": "SUV",
  "motor_type": "Gasoline",
  "mileage": 55830.25
}
```

---

#### 2. `GET /vehicles`

**Descripción:** Retorna todos los vehículos registrados en la base de datos.

---

#### 3. `GET /vehicles/{id}`

**Descripción:** Retorna la información de un vehículo específico mediante su ID generado por MongoDB.
**Ejemplo de uso:**
`GET /vehicles/68dec392299728ecf819c8bb`

---

#### 4. `PUT /vehicles/{id}`

**Descripción:** Actualiza los datos de un vehículo existente.
**Ejemplo de cuerpo (JSON):**

```json
{
  "brand": "Ford",
  "model": "Explorer",
  "year": 2022,
  "price": 245000000,
  "category": "SUV",
  "motor_type": "Gasoline",
  "mileage": 55830.25
}
```

---

#### 5. `DELETE /vehicles/{id}`

**Descripción:** Elimina un vehículo existente a partir de su ID.
**Ejemplo:**
`DELETE /vehicles/68dec392299728ecf819c8bb`

---

### Modelo de datos

Definido con **Pydantic** y **Typing**:

```python
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
```

---

### Seguridad y autenticación

Actualmente, el microservicio **no implementa autenticación ni middleware de seguridad**.
En la lógica de negocio se considera que, por el momento, **solo los administradores** pueden agregar o modificar vehículos.
En futuras versiones se añadirá **autenticación mediante tokens Bearer** generados por el microservicio de autenticación.

---

### Comunicación con otros microservicios

El microservicio **Vehicle Catalog** es **consumido por**:

* **Microservicio de Reportes** → Generación de reportes PDF y Excel.
* **Microservicio de Publicaciones y Ventas** → Para obtener información del inventario de vehículos disponible.

Las interacciones se realizan mediante peticiones HTTP `GET` desde los otros microservicios hacia este servicio.

---

### Ejecución del microservicio

1. Asegúrarse de tener **Python 3.13.3** y **MongoDB** instalados y en ejecución.
2. Instala las dependencias:

   ```bash
   pip install -r requirements.txt
   ```
3. Ejecuta el servicio (desde **fuera** de la carpeta del proyecto):

   ```bash
   uvicorn Microservice_VehicleCatalog.main:app --reload --port 8001
   ```
4. Acceder a la documentación automática de la API en:
   👉 [http://localhost:8001/docs](http://localhost:8001/docs)

---

### Pruebas de rendimiento

Se realizaron pruebas de **carga y capacidad** con **Locust**, cuyos archivos se encuentran en el repositorio.

---

### Futuras implementaciones

* Protección de rutas mediante autenticación con token Bearer.
* Contenedorización con **Docker**.
* Orquestación con **Kubernetes**.
* Implementación de búsquedas y filtros avanzados.

---

### Licencia

MIT (heredada de la plantilla base de Laravel).

---

### Contacto / Mantenimiento

* **Autor:** Juan David Fajardo Betancourt
* **Email:** [jfajardob@unal.edu.co](mailto:jfajardob@unal.edu.co)

---

### Razón

* Proyecto semestral de **Ingeniería de Software II**, semestre **2025-2**.
* Presentado al docente: **Jose Albeiro Montes Gil**.
* Documento de planeación: *[https://docs.google.com/document/d/1bnb3KTs5Pmeoy83xN5RjugHqdJ3E_rLXUf8NLsQU5xE/edit?usp=sharing](https://docs.google.com/document/d/1bnb3KTs5Pmeoy83xN5RjugHqdJ3E_rLXUf8NLsQU5xE/edit?usp=sharing)*
* Informe de evidencia de ejecución de pruebas de rendimiento: *[https://docs.google.com/document/d/1S7h12ZzESNoP5FUDjKQ7n9BWXnBOSWf8oHqbKiwUuSc/edit?usp=sharing](https://docs.google.com/document/d/1S7h12ZzESNoP5FUDjKQ7n9BWXnBOSWf8oHqbKiwUuSc/edit?usp=sharing)*