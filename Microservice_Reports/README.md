# Microservicio de Reportes - Concesionario de Vehículos

Este microservicio permite la **generación de reportes en formato PDF y Excel** basados en los datos proporcionados por otros microservicios del ecosistema del concesionario de vehículos.  
Está desarrollado en **Python 3.13.3** utilizando **Flask** como framework principal y bibliotecas especializadas para la generación de documentos (ReportLab y OpenPyXL).  
Su uso está restringido únicamente a **usuarios con rol de administrador**, autenticados mediante **tokens Bearer** generados por el microservicio de autenticación.

---

### Tecnologías y dependencias principales

- **Lenguaje:** Python 3.13.3  
- **Framework:** Flask  
- **Librerías principales:**
  - `pandas`
  - `reportlab` (para generación de PDF)
  - `openpyxl` (para exportación a Excel)
  - `requests` (para consultar otros microservicios)

> **Nota:** No hay versiones específicas de los paquetes.  
> Todas las dependencias deben instalarse ejecutando:
> ```bash
> pip install -r requirements.txt
> ```

---

### Configuración

No requiere variables de entorno personalizadas.  
El microservicio **consume tokens Bearer** generados desde el microservicio de autenticación.  
El token se envía en el encabezado `Authorization` dentro de Postman o Thunder Client de la siguiente manera:

````

Authorization: Bearer <TOKEN_ADMIN>
Content-Type: application/json

````

---

### Ejecución del microservicio

1. Asegurarse de tener **Python 3.13.3** u otra version instalada.  
2. Instala las dependencias:

```bash
   pip install -r requirements.txt
```

1. Ejecuta el servidor Flask:

   ```bash
   flask --app app run
   ```

---

### Endpoints disponibles

#### 1. `/reports/pdf`

* **Método:** `POST`
* **Descripción:** Genera un reporte PDF a partir de los datos obtenidos desde otro microservicio.
* **Cuerpo de la solicitud:**

  ```json
  {
    "ms_url": "http://localhost:8000/api/users"
  }
  ```

* **Encabezados requeridos:**

  ```
  Authorization: Bearer <TOKEN_ADMIN>
  Content-Type: application/json
  ```

* **Ejemplo de uso:**
  En Postman, envía una solicitud POST a `http://localhost:5000/reports/pdf` con el body anterior.
  El sistema devolvera un 200 y un archivo PDF descargable desde el save response to file con los datos obtenidos.

---

#### 2. `/reports/excel`

* **Método:** `POST`
* **Descripción:** Genera un reporte Excel (`.xlsx`) desde otro microservicio.
* **Cuerpo de la solicitud:**

  ```json
  {
    "ms_url": "http://localhost:8002/api/vehicles"
  }
  ```

* **Encabezados requeridos:**

  ```
  Authorization: Bearer <TOKEN_ADMIN>
  Content-Type: application/json
  ```

* **Ejemplo de uso:**
  `http://localhost:5000/reports/excel`

---

### Seguridad y restricciones

* Solo **administradores** pueden usar este microservicio.
* Si el token enviado no es válido o ha expirado, la petición será **rechazada**.
* El microservicio **no almacena información**; únicamente genera reportes basados en datos de otros servicios.

---

### Microservicios consumidos

El microservicio de reportes realiza consultas hacia:

* **Microservicio de Autenticación** (para validar el token y reportar usuarios de la base de datos).
* **Microservicio de Catálogo de Vehículos**.
* **Microservicio de Publicaciones y ventas.**

Las consultas se realizan mediante peticiones de tipo **POST** enviando la URL del endpoint GET de cada servicio en el campo `ms_url`.

---

### Pruebas de rendimiento

Se realizaron **pruebas de carga y capacidad** utilizando **Locust**.
Los archivos `.py` correspondientes a dichas pruebas se encuentran incluidos en el repositorio.
Un informe completo con los resultados y análisis se adjuntará en un **documento de Google Drive** enlazado próximamente.

---

### Contenerización con docker 

Para la segunda entrega del proyecto se contenerizaron los servicios del proyecto mediante un archivo docker compose, a continuación se presenta el fragmento del docker compose y el dockefile correspondiente a este microservicio:

```Docker
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
```

```Docker-compose
# ------------------------------------------------------------
  # Microservicio Reportes (Flask)
  # ------------------------------------------------------------
  reports-ms:
    build:
      context: ./Microservice_Reports
      dockerfile: ../Dockerfile-reports
    container_name: reports-ms
    env_file:
      - ./Microservice_Reports/.env.docker
    ports:
      - "5000:5000"
    depends_on:
      - auth-ms
      - sales-ms
      - catalog-ms
    volumes:
      - ./Microservice_Reports:/app
    networks:
      red_publica:
        ipv4_address: 192.168.100.23
```

---

### Futuras implementaciones

* Integración de **Kubernetes** para orquestación y despliegue.
* Posible extensión para generación de reportes dinámicos y gráficos visuales.

---

### Licencia

MIT.

---

### Contacto / Mantenimiento

* **Autor:** Juan David Fajardo Betancourt
* **Email:** [jfajardob@unal.edu.co](mailto:jfajardob@unal.edu.co)

---

### Razón

* Proyecto semestral de **Ingeniería de Software II**, semestre **2025-2**.
* Presentado al docente: **Jose Albeiro Montes Gil**.
* [Documento de planeación](https://docs.google.com/document/d/1bnb3KTs5Pmeoy83xN5RjugHqdJ3E_rLXUf8NLsQU5xE/edit?usp=sharing)
* [Informe de evidencia de ejecución de pruebas de rendimiento](https://docs.google.com/document/d/1S7h12ZzESNoP5FUDjKQ7n9BWXnBOSWf8oHqbKiwUuSc/edit?usp=sharing)
