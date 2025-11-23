# Microservice Authentication – Concesionario de Vehículos

Este es un servicio de autenticación y gestión básica de identidades para un ecosistema modular (microservicios) de un aplicativo web de un concesionario de vehículos como parte del proyecto semestral de **Ingeniería de Software II**.  
Provee registro de usuarios, inicio/cierre de sesión mediante tokens personales (**Laravel Sanctum**), asignación automática de rol inicial, protección por middleware y soporte para pruebas unitarias.  
Está diseñado para operar de forma independiente y ser consumido por otros servicios pertenecientes del aplicativo bajo una arquitectura de microservicios propuesta.

---

### Información técnica

- **Lenguaje:** PHP 8.2.12  
- **Framework:** Laravel 10  
- **Autenticación:** Laravel Sanctum  
- **Base de datos:** MySQL  
- **Servidor local:** Laragon  
- **Pruebas de rendimiento:** Locust  
- **Arquitectura:** Microservicio independiente

---

### Instalación y ejecución

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/Therealdavi836/Microservice_Authentication.git
   cd Microservice_Authentication
   ```

2. **Instalar dependencias**
   ```bash
   composer update
   ```

3. **Configurar entorno**
   Crea un archivo `.env` basado en `.env.example` y definir la conexión a base de datos MySQL:
   ```env
   DB_CONNECTION=mysql
   DB_HOST=127.0.0.1
   DB_PORT=3306
   DB_DATABASE=nombre_de_tu_bd
   DB_USERNAME=root
   DB_PASSWORD=
   ```
   > El nombre de la base de datos debe coincidir con el que se crea en Laragon.

4. **Ejecutar migraciones y seeders**
   ```bash
   php artisan migrate --seed
   ```
   Esto creará la tabla `users` y los roles iniciales:
   | Rol      | ID |
   | -------- | -- |
   | Admin    | 1  |
   | Seller   | 2  |
   | Customer | 3  |
   | Support  | 4  |

5. **Iniciar el servidor**
   ```bash
   php artisan serve
   ```
   El microservicio estará disponible en `http://127.0.0.1:8000`.

---

### Endpoints disponibles

| Método | Ruta        | Descripción                                 | Autenticación |
| ------ | ----------- | ------------------------------------------- | ------------- |
| `POST` | `/register` | Registra un nuevo usuario.                  | ❌             |
| `POST` | `/login`    | Inicia sesión y devuelve un token Bearer.   | ✅             |
| `POST` | `/logout`   | Cierra sesión y revoca el token actual.     | ✅ (Bearer)    |
| `GET`  | `/user`     | Devuelve los datos del usuario autenticado. | ✅ (Bearer)    |

---

### Ejemplo de uso (Postman o Thunder Client)

1. Ejecutar `POST /login` con credenciales válidas.
2. Copiar el token recibido.
3. En la pestaña **Auth → Bearer Token**, pegar el token.
4. Probar el endpoint `GET /user` o `POST /logout` para validar autenticación.

> Solo los usuarios con rol **Admin** pueden acceder a rutas protegidas de gestión de usuarios.

---

### Pruebas de rendimiento

Se implementaron pruebas de **carga y rendimiento** con **Locust**.
El informe detallado de dichas pruebas se encuentra disponible en un documento compartido de Google Drive anexado al informe del proyecto.

---

### Contenerización con docker 

Para la segunda entrega del proyecto se contenerizaron los servicios del proyecto mediante un archivo docker compose, a continuación se presenta el fragmento del docker compose y el dockefile correspondiente a este microservicio:
   ```Docker
   FROM php:8.2-fpm

   # Sistema y extensiones
   RUN apt-get update && apt-get install -y \
      git unzip libzip-dev libonig-dev libpng-dev libicu-dev zlib1g-dev \
      default-mysql-client \
   && docker-php-ext-install pdo_mysql mbstring exif pcntl bcmath zip intl

   # Composer
   COPY --from=composer:2 /usr/bin/composer /usr/bin/composer

   WORKDIR /var/www/html

   # Copiar composer files primero para cache
   COPY composer.json composer.lock ./
   RUN composer install --no-dev --prefer-dist --no-interaction --no-plugins --no-scripts || true

   # Copiar todo el código
   COPY . .

   # Permisos
   RUN chown -R www-data:www-data /var/www/html/storage /var/www/html/bootstrap/cache \
   && chmod -R 755 /var/www/html/storage /var/www/html/bootstrap/cache

   EXPOSE 8000

   # Nota: ejecutamos artisan serve para desarrollo; en producción usar PHP-FPM + nginx.
   CMD ["sh", "-c", "php artisan key:generate --force || true && php artisan migrate --force || true && php artisan serve --host=0.0.0.0 --port=8000"]
   ```
   ```Docker-compose
   # ------------------------------------------------------------
   # Microservicio AUTH (Laravel + Gateway)
   # ------------------------------------------------------------
   auth-ms:
      build:
         context: ./Microservice_Authentication
         dockerfile: ../Dockerfile-auth
      container_name: auth-ms
      env_file:
         - ./Microservice_Authentication/.env.docker
      ports:
         - "8000:8000"
      depends_on:
         mysql:
         condition: service_healthy
      volumes:
         - ./Microservice_Authentication:/var/www/html
      networks:
         red_publica:
         ipv4_address: 192.168.100.20
   ```

### Contenido próximo a implementar

* Orquestación con **Kubernetes**.
* Recuperación de contraseñas.
* Refresco de tokens.

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
* [Documento de planeación](https://docs.google.com/document/d/1bnb3KTs5Pmeoy83xN5RjugHqdJ3E_rLXUf8NLsQU5xE/edit?usp=sharing)
* [Informe de evidencia de ejecución de pruebas de rendimiento](https://docs.google.com/document/d/1S7h12ZzESNoP5FUDjKQ7n9BWXnBOSWf8oHqbKiwUuSc/edit?usp=sharing)
