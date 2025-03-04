# 🎮 API de Torneos y Juegos

## 📌 Descripción
Esta API permite gestionar torneos, juegos, participantes y equipos, asegurando que solo los usuarios con los permisos adecuados puedan realizar ciertas acciones.

---

## 🔐 Autenticación y Permisos

La API usa **OAuth2** con tokens de acceso para autenticar usuarios. Además, emplea **permisos en Django** para restringir el acceso a ciertas operaciones.

### 📌 **Roles y Permisos**  

| Rol        | Permisos |
|------------|---------|
| **Jugador** | ✅ Puede ver torneos, juegos y participantes. ❌ No puede crear, editar ni eliminar nada. |
| **Organizador** | ✅ Puede crear, editar y eliminar torneos y juegos. |
| **Administrador** | ✅ Tiene acceso total a todas las operaciones. |

### 📌 **Uso del Token de Autenticación**
Cuando un usuario inicia sesión, obtiene un `access_token` que debe incluir en cada petición autenticada:

```http
Authorization: Bearer <token>



## 🚀 Despliegue con Docker

### 🐳 **Iniciar la API con Docker**
Para construir y ejecutar la API, usa:

```sh
docker compose up --build

### 🐳 **Detener la API con Docker**
docker compose down