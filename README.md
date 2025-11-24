# Proyecto de Concesionario Web

Repositorio con el proyecto de Ingeniería de Software II.

## Descripción

Este proyecto corresponde a un sistema de concesionario web desarrollado como parte de la asignatura **Ingeniería de Software II**, bajo la dirección del docente **Jose Albeiro Montes Gil**. El objetivo principal es la implementación de una arquitectura basada en microservicios, donde cada funcionalidad principal del sistema está desacoplada y mantenida de forma independiente.

## Arquitectura

El sistema está compuesto por múltiples microservicios, cada uno encargado de una funcionalidad específica del concesionario (por ejemplo, autenticación, inventario de vehículos, ventas, etc.). Cada microservicio posee su propio repositorio individual, el cual incluye sus respectivas instrucciones de instalación, despliegue y uso. Esto permite un desarrollo, mantenimiento y escalabilidad independiente de cada componente.

> **Nota:** Puede consultar cada repositorio de microservicio para obtener instrucciones detalladas de instalación y uso.

## Repositorios de microservicios
- [Microservicio de Autenticación](https://github.com/Therealdavi836/Microservice_Authentication.git)
- [Microservicio de Reportes](https://github.com/Therealdavi836/Microservice_Reports.git)
- [Microservicio de Catalogo de Vehiculos](https://github.com/Therealdavi836/Microservice_VehicleCatalog.git)
- [Microservicio de Publicaciones y Ventas](https://github.com/Therealdavi836/Microservice_SalesPublications.git)
- [Microservicio de Notificaciones](https://github.com/Therealdavi836/Microservice_Notifications.git)

## Organización del proyecto

- Este repositorio es el punto central de coordinación del proyecto.
- Cada microservicio se encuentra en su propio repositorio independiente.
- Para desplegar el sistema completo, sigue las instrucciones de cada microservicio según el orden y dependencias especificadas en sus respectivos repos.

## Actualización de los avances del proyecto - Contenerización con docker

Para la segunda entrega de hoy domingo 23 de noviembre del 2025, se requirió de contenerizar los microservicios del aplicativo en consecuencia con sus bases de datos, para presentación de resultados se construyeron 5 dockerfiles especificos por cada microservicio con las bases de datos que se hicieron directamente desde DockerHuB, a continuación se presenta una sección explicando los detalles implementados en la entrega

## Acceso de Puertos por Microservicio

Cada microservicio del ecosistema expone su propia interfaz a través de un puerto específico dentro del entorno Docker:

| Microservicio          | Puerto |
| ---------------------- | ------ |
| Autenticación          | 8000   |
| Catálogo de Vehículos  | 8001   |
| Publicaciones y Ventas | 8002   |
| Notificaciones         | 8003   |
| Reportes               | 5000   |
| MongoDB                | 27017  |
| MySQL                  | 3306   |

## Uso del Aplicativo

Registro e inicio de sesión

- El registro asigna automáticamente el rol **customer**.
- Los administradores pueden modificar roles cuando sea necesario.

| Acción         | Método | URL                                  |
| -------------- | ------ | ------------------------------------ |
| Registrar      | POST   | `http://localhost:8000/api/register` |
| Iniciar sesión | POST   | `http://localhost:8000/api/login`    |
| Cerrar sesión  | POST   | `http://localhost:8000/api/logout`   |

Módulo de Reportes

Requisitos:

- Solo accesible por usuarios con rol Administrator.

- La petición debe incluir los headers:

```Bash
Authorization: Bearer <Token_Bearer generado del login>

Content-Type: application/json

Accept: application/json

Endpoint del MS de reportes:

POST http://localhost:5000/report/pdf

POST http://localhost:5000/report/excel
```

Fuentes de información usadas por el módulo de reportes (Cambian las url al contenerizar con red interna)

Usuarios
`"ms_url": "http://192.168.100.20:8000/api/users"`

Vehículos
`"ms_url": "http://auth-ms:8000/api/forward/catalog/vehicle"`

Publicaciones (No paso directo por petición forward del gateway como lo hacen vehiculos)

`"ms_url": "http://auth-ms:8000/api/forward/publications"`

`"ms_url": "http://sales-ms:8002/api/publications"`

Ventas(Repite el caso anterior al estar en el mismo microservicio)

`"ms_url": "http://sales-ms:8002/api/sales"`

## Uso del Microservicio de Vehículos

Operaciones CRUD a través del gateway (Auth-MS):

`http://localhost:8000/api/forward/catalog/vehicles`


Ejemplo de cuerpo (POST):

```JSON
{
  "brand": "Tesla",
  "model": "model y",
  "year": 2025,
  "price": 119000000,
  "category": "SUV",
  "motor_type": "hybrid",
  "mileage": 0
}
```
Ejemplo de cuerpo (PUT):

```JSON
{
  "id": "692392c30bd0114777b8d888"
  "brand": "Tesla",
  "model": "model y",
  "year": 2025,
  "price": 119000000,
  "category": "SUV",
  "motor_type": "hybrid",
  "mileage": 0
}
```

El parámetro id se usa únicamente en PUT y DELETE de la siguiente forma:

`http://localhost:8000/api/forward/catalog/vehicles/692392c30bd0114777b8d888`

## Uso del Microservicio de Publicaciones y Ventas

Este microservicio no puede ser consumido mediante el gateway debido a problemas internos de reenvío de cuerpo y autenticación.
Por lo tanto, debe accederse directamente:

`http://localhost:8002/api/publications`

- GET para todas las publicaciones

- GET con {id}

- PUT con {id}

- DELETE con {id}

Ejemplo POST:

```JSON
{
  "vehicle_id": "692392c30bd0114777b8d888",
  "title": "Nuevo Tesla Model Y compra directa en Colombia",
  "description": "Se vende nuevo Tesla Model Y con concesionaria directa en Colombia",
  "price": 119000000
}
```

Ejemplo de respuesta:

```JSON
{
  "user_id": 2,
  "vehicle_id": "692392c30bd0114777b8d888",
  "title": "Nuevo Tesla Model Y compra directa en Colombia",
  "description": "Se vende nuevo Tesla Model Y con concesionaria directa en Colombia",
  "price": 119000000,
  "status": "activo",
  "updated_at": "2025-11-23T23:10:53.000000Z",
  "created_at": "2025-11-23T23:10:53.000000Z",
  "id": 3
}
```

Para las ventas se cuenta con la misma situación.

Acceso directo:

`http://localhost:8002/api/sales`


Solo roles admin y customer.

Solo aplica:

- GET general

- GET por id

- POST para crear la venta

Cuerpo de venta (POST):

```JSON
{
  "publication_id": "3",
  "sale_price": 119000000
}
```

Ejemplo de respuesta:

```JSON
{
  "publication_id": 3,
  "customer_id": 3,
  "seller_id": 2,
  "sale_price": 119000000,
  "sale_date": "2025-11-23T23:18:21.779297Z",
  "updated_at": "2025-11-23T23:18:21.000000Z",
  "created_at": "2025-11-23T23:18:21.000000Z",
  "id": 2
}
```

## Notificaciones

El sistema genera notificaciones automáticas por eventos clave:

- Creación de usuario (registro)

- Publicaciones

- Ventas

- Operaciones respecto a la integración de vehiculos en el catalogo

## Razón de Diferencias entre Dockerfiles

Cada microservicio posee un Dockerfile distinto debido a:

- Microservicios en Python

- Requieren requirements.txt diferenciales en cuanto a la logica de cada microservicio.

- Usan distintos frameworks (FastAPI, Django, Flask).

- Tienen rutas internas, dependencias y estructuras de carpetas independientes.

Se ejecutan con comandos distintos:

- gunicorn

- uvicorn

- python app.py

## Microservicios en PHP/Laravel (Auth y Publications/Sales)

Ambos requieren PHP 8.2 y extensiones iguales.

Sin embargo, están en repositorios y proyectos diferentes con:

- Migraciones independientes

- Dependencias de Composer distintas

- Estructuras propias de almacenamiento

- Endpoints expuestos y puertos diferentes

Por eso los contenedores deben construirse por separado, aunque ambos usen Laravel.

## Bases de datos

Se construyeron las bases de datos (MySQL y Mongo) en el archivo de Docker-compose.yaml de la siguiente manera, para la base de datos de MySQL se incluyo un archivo de inicialización para crear las bases de datos automaticamente dentro de los contenedores, el servicio de mongo no necesita script automatico, con solo añadir un registro crea la base automaticamente con su colección asociada segun FastAPI

```Docker-compose
# ------------------------------------------------------------
  # Base de datos MySQL (Auth, SalesPublications, Notifications)
  # ------------------------------------------------------------
  mysql:
    image: mysql:8.0
    container_name: mysql
    environment:
      MYSQL_ROOT_PASSWORD: rootpass
      MYSQL_DATABASE: microservice_authentication
    volumes:
      - mysql_data:/var/lib/mysql
      - ./docker/mysql:/docker-entrypoint-initdb.d
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      red_publica:
        ipv4_address: 192.168.100.10

  # ------------------------------------------------------------
  # Base de datos Mongo (Vehicle Catalog)
  # ------------------------------------------------------------
  mongo:
    image: mongo:6.0
    container_name: mongo
    volumes:
      - mongo_data:/data/db
    healthcheck:
      test: ["CMD", "mongosh", "--eval", "db.adminCommand('ping')"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      red_publica:
        ipv4_address: 192.168.100.11
```
Ambos contenedores ejecutan un chequeo de salud para validar funcionamiento y monitorización.

## Licencia

MIT

## Contacto / Mantenimiento

- **Autor:** Juan David Fajardo Betancourt  
- **Email:** jfajardob@unal.edu.co

## Razón

Proyecto semestral de Ingeniería de Software II, semestre 2025-2.  
Presentado al docente: **Jose Albeiro Montes Gil**.

- [Documento de planeación](https://docs.google.com/document/d/1bnb3KTs5Pmeoy83xN5RjugHqdJ3E_rLXUf8NLsQU5xE/edit?usp=sharing)
- [Informe de evidencia de ejecución de pruebas de rendimiento](https://docs.google.com/document/d/1S7h12ZzESNoP5FUDjKQ7n9BWXnBOSWf8oHqbKiwUuSc/edit?usp=sharing)

---
Para más detalles, puede revisar la documentación incluida en cada microservicio.
