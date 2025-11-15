# Microservice Notifications – Concesionario de Vehículos

Este microservicio, desarrollado en **Django REST Framework (Python 3.13.3)**, permite gestionar y enviar **notificaciones automáticas** (email y SMS) entre los distintos módulos del ecosistema de microservicios del concesionario de vehículos.  
Su función principal es recibir solicitudes desde otros microservicios (como autenticación, catálogo de vehículos y ventas/publicaciones) para crear y distribuir notificaciones a los usuarios correspondientes.

---

## Características principales

- Recepción de notificaciones vía **API REST** desde otros microservicios.
- Soporte de **correo electrónico** mediante SMTP (Gmail) y envío de **mensajes SMS** a través de **Twilio**.
- Implementado con **Django REST Framework 3.15.0** y **Django 5.2.0**.
- Almacenamiento en **MySQL**, administrado mediante **ORM de Django**.
- **CORS habilitado** para permitir peticiones desde microservicios en Laravel y FastAPI.
- API expuesta en el puerto **8003**.
- Reportes de rendimiento con pruebas de **carga y capacidad** ejecutadas con Locust.
- Preparado para integración futura con **Docker** y **Kubernetes**.

---

## Dependencias principales

Archivo `requirements.txt`:

```txt
Django==5.2.0
djangorestframework==3.15.0
django-cors-headers==4.0.0
python-dotenv==1.0.0
twilio==8.2.0
mysqlclient==2.2.0
gunicorn==21.2.0

---

## Configuración y variables de entorno

Archivo `.env`:

```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu_correo
EMAIL_HOST_PASSWORD=(Generarlo desde app password de google)
NOTIFICATION_EMAIL=tu_correo

TWILIO_ACCOUNT_SID=tu_sid
TWILIO_AUTH_TOKEN=tu_token
TWILIO_PHONE_NUMBER=tu_numero_de_prueba
MY_PHONE_NUMBER=tu_numero_real
```

> ⚠️ **Importante:** Las credenciales aquí son de ejemplo y deben ser reemplazadas por variables seguras en producción y es necesario crear una cuenta en twilio para poner los datos anteriores.

---

## Base de datos

El microservicio utiliza **MySQL**.
Configuración por defecto en `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'microservice_notifications',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

Antes de ejecutar el servidor, crear la base de datos manualmente (por ejemplo, en **Laragon** o **MySQL Workbench**) y correr las migraciones:

```bash
python manage.py migrate
```

---

## Modelo de datos

`models.py`:

```python
from django.db import models

class Notification(models.Model):
    user_id = models.IntegerField()  # viene del Auth MS (no FK real)
    title = models.CharField(max_length=255)
    message = models.TextField()
    type_choices = [
        ('info', 'Info'),
        ('warning', 'Warning'),
        ('success', 'Success'),
        ('error', 'Error'),
        ('publication', 'Publication'),
        ('sales', 'Sales'),
        ('system', 'System'),
    ]
    type = models.CharField(max_length=50, choices=type_choices)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} -> User {self.user_id}"
```

---

## Endpoints principales

El microservicio expone sus rutas mediante **Django REST Framework Router**.

Ruta base: `http://127.0.0.1:8003/api/notifications/`

| Método     | Endpoint                   | Descripción                                 |
| :--------- | :------------------------- | :------------------------------------------ |
| **GET**    | `/api/notifications/`      | Lista todas las notificaciones.             |
| **POST**   | `/api/notifications/`      | Crea una nueva notificación.                |

Ejemplo de solicitud **POST**:

```json
{
  "user_id": 12,
  "title": "Nueva publicación disponible",
  "message": "El vehículo Ford Explorer ha sido publicado.",
  "type": "publication"
}
```

Ejemplo de respuesta exitosa (**201 Created**):

```json
{
  "id": 45,
  "user_id": 12,
  "title": "Nueva publicación disponible",
  "message": "El vehículo Ford Explorer ha sido publicado.",
  "type": "publication",
  "is_read": false,
  "created_at": "2025-10-07T15:32:44Z"
}
```

---

## Integración con otros microservicios

Este microservicio es **consumido** por:

* **Microservicio de Vehículos** (para notificar sobre publicaciones nuevas o actualizaciones)
* **Microservicio de Publicaciones y Ventas** (para notificar ventas, cambios de estado, etc.)
* **Microservicio de Autenticación** (para notificaciones del sistema o usuarios)

No utiliza autenticación JWT, ya que solo recibe información estructurada y el `user_id` desde los otros microservicios.

Comunicación vía **HTTP REST** con solicitudes tipo `POST` hacia:

```API
http://127.0.0.1:8003/api/notifications/
```

---

## Instalación y ejecución

```bash
# Instalar dependencias
pip install -r requirements.txt

# Crear base de datos en MySQL (nombre: microservice_notifications)

# Ejecutar migraciones
python manage.py migrate

# Iniciar el servidor
python manage.py runserver 8003
```

---

## Pruebas de rendimiento

* Se realizaron **pruebas de carga y capacidad** con **Locust**.
* Los archivos de prueba están en el repositorio.
* El informe con resultados y análisis se encuentra disponible en el siguiente documento:

---

## Roadmap futuro

* Integrar servicios de correo **profesionales** (SendGrid o AWS SES).
* Incorporar **WebSockets o Firebase Cloud Messaging** para notificaciones en tiempo real.
* Implementar **Docker y Kubernetes** para orquestación.
* Filtrado y paginación avanzada de notificaciones.

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
