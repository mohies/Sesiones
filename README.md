# Documentación del Proyecto

## Tipos de Usuarios

En la aplicación existen tres tipos de usuarios: **Administrador**, **Jugador** y **Organizador**. Cada uno tiene permisos y funcionalidades diferenciadas dentro de la plataforma.

### 1. **Administrador**
   El administrador tiene acceso completo a todas las funcionalidades de la aplicación, tales como:
   - **Crear**, **editar** y **eliminar** torneos.
   - **Ver** todos los torneos y la información de los jugadores.
   - **Gestionar** los usuarios (jugadores y organizadores).
   - Acceso a **funcionalidades administrativas** del sistema.
   
   **Nota:** Los administradores no tienen un rol asignado en el modelo de usuario ya que están predefinidos por el sistema de autenticación de Django.

### 2. **Jugador**
   Los jugadores tienen permisos más limitados. Las funcionalidades a las que pueden acceder son:
   - **Ver los torneos** en los que están inscritos.
   - **Inscribirse** en torneos disponibles.
   - **Visualizar su perfil** y estadísticas de participación.
   - Participar en torneos y ver clasificaciones.
   
   **Restricciones:**
   - Los jugadores no pueden crear ni eliminar torneos.
   - Los jugadores solo pueden ver torneos a los que están inscritos.

### 3. **Organizador**
   Los organizadores son responsables de crear y gestionar torneos. Pueden acceder a las siguientes funcionalidades:
   - **Crear** torneos nuevos.
   - **Editar** los torneos que han creado.
   - **Eliminar** torneos (si es necesario).
   - **Ver** los torneos que han creado y su información relacionada (participantes, jugadores, etc.).
   
   **Restricciones:**
   - Los organizadores no pueden ver ni modificar los torneos de otros organizadores ni jugadores.
   - Los organizadores no pueden eliminar ni gestionar usuarios.

---

## Acceso a Funcionalidades

Cada tipo de usuario tiene diferentes permisos según su rol y el tipo de operación. El sistema controla el acceso de los usuarios a las vistas mediante los decoradores `@login_required`, `@permission_required`, y `@user_passes_test`. Además, las vistas están configuradas para mostrar diferentes opciones de acuerdo al grupo al que pertenece el usuario.

### Control de Acceso:
- **Jugadores** pueden acceder únicamente a las vistas relacionadas con su participación en torneos.
- **Organizadores** tienen acceso a la creación y edición de torneos.
- **Administradores** tienen acceso completo a todas las vistas y funcionalidades.

---

# Documentación del Proyecto

## Tipos de Usuarios

En la aplicación existen tres tipos de usuarios: **Administrador**, **Jugador** y **Organizador**. Cada uno tiene permisos y funcionalidades diferenciadas dentro de la plataforma.

### 1. **Administrador**
   El administrador tiene acceso completo a todas las funcionalidades de la aplicación, tales como:
   - **Crear**, **editar** y **eliminar** torneos.
   - **Ver** todos los torneos y la información de los jugadores.
   - **Gestionar** los usuarios (jugadores y organizadores).
   - Acceso a **funcionalidades administrativas** del sistema.
   
   **Nota:** Los administradores no tienen un rol asignado en el modelo de usuario ya que están predefinidos por el sistema de autenticación de Django.

### 2. **Jugador**
   Los jugadores tienen permisos más limitados. Las funcionalidades a las que pueden acceder son:
   - **Ver los torneos** en los que están inscritos.
   - **Inscribirse** en torneos disponibles.
   - **Visualizar su perfil** y estadísticas de participación.
   - Participar en torneos y ver clasificaciones.
   
   **Restricciones:**
   - Los jugadores no pueden crear ni eliminar torneos.
   - Los jugadores solo pueden ver torneos a los que están inscritos.

### 3. **Organizador**
   Los organizadores son responsables de crear y gestionar torneos. Pueden acceder a las siguientes funcionalidades:
   - **Crear** torneos nuevos.
   - **Editar** los torneos que han creado.
   - **Eliminar** torneos (si es necesario).
   - **Ver** los torneos que han creado y su información relacionada (participantes, jugadores, etc.).
   
   **Restricciones:**
   - Los organizadores no pueden ver ni modificar los torneos de otros organizadores ni jugadores.
   - Los organizadores no pueden eliminar ni gestionar usuarios.

---

## Acceso a Funcionalidades

Cada tipo de usuario tiene diferentes permisos según su rol y el tipo de operación. El sistema controla el acceso de los usuarios a las vistas mediante los decoradores `@login_required`, `@permission_required`, y `@user_passes_test`. Además, las vistas están configuradas para mostrar diferentes opciones de acuerdo al grupo al que pertenece el usuario.

### Control de Acceso:
- **Jugadores** pueden acceder únicamente a las vistas relacionadas con su participación en torneos.
- **Organizadores** tienen acceso a la creación y edición de torneos.
- **Administradores** tienen acceso completo a todas las vistas y funcionalidades.

---


# 🎮 **Torneo API**  
API para la gestión de torneos, participantes, equipos, juegos y más. Este proyecto proporciona endpoints para gestionar y consultar información sobre torneos, equipos, participantes, jugadores, juegos, y sus relaciones.

---

## 📋 **Descripción**  
La API está construida usando **Django Rest Framework (DRF)** y está diseñada para facilitar la interacción con una base de datos relacionada con torneos. Permite gestionar usuarios, torneos, equipos, jugadores y otras entidades del ecosistema de un torneo de videojuegos.

### **Modelo de datos principal**:
- **Usuario**: Representa a los usuarios que pueden ser jugadores, organizadores o espectadores.
- **Torneo**: Representa los eventos donde se llevan a cabo las competiciones.
- **Equipo**: Representa los equipos que participan en los torneos.
- **Jugador**: Jugadores que forman parte de los equipos en un torneo.
- **Juego**: Los juegos en los que se compite.
- **Participante**: Participantes que están inscritos en un torneo.

---

## 🛠 **Serializadores**  
Los **serializadores** definen cómo se transforman los modelos de la base de datos en JSON para ser consumidos por la API. A continuación se describen los serializadores principales:

### **Serializadores básicos**:

- **`UsuarioLoginSerializer`**:  
  Serializa el modelo `UsuarioLogin`, que gestiona la autenticación del usuario.

- **`OrganizadorSerializer`**:  
  Serializa el modelo `Organizador`, que se asocia a un usuario (a través de `UsuarioLoginSerializer`).

- **`UsuarioSerializer`**:  
  Serializa el modelo `Usuario`, que incluye información básica del usuario.

- **`PerfilDeJugadorSerializer`**:  
  Serializa el modelo `PerfilDeJugador`, que incluye detalles sobre un jugador, incluyendo su usuario.

- **`EquipoSerializer`**:  
  Serializa el modelo `Equipo`, que representa a un equipo en el sistema.

- **`ParticipanteSerializer`**:  
  Serializa el modelo `Participante`, que representa a un jugador o equipo participante en un torneo. Incluye relaciones con el modelo `Usuario` y `Equipo`.

- **`TorneoSerializer`**:  
  Serializa el modelo `Torneo` y incluye la relación con los participantes del torneo mediante `ParticipanteSerializer`.

- **`JugadorSerializer`**:  
  Serializa el modelo `Jugador`, que está asociado a un usuario y varios torneos. Incluye detalles como el usuario y los torneos en los que participa.

- **`ConsolaSerializer`**:  
  Serializa el modelo `Consola`, que contiene información sobre las consolas usadas en los torneos.

- **`JuegoSerializer`**:  
  Serializa el modelo `Juego`, que representa los videojuegos en los que se juega en los torneos. Incluye relaciones con el torneo y la consola.

- **`EspectadorSerializer`**:  
  Serializa el modelo `Espectador`, que representa a los usuarios que no participan directamente, pero siguen los torneos.

- **`ClasificacionSerializer`**:  
  Serializa el modelo `Clasificacion`, que representa la posición de un participante en un torneo.

- **`ParticipanteEquipoSerializer`**:  
  Serializa la relación entre participantes y equipos. Muestra la conexión entre un jugador y su equipo.

- **`TorneoJuegoSerializer`**:  
  Serializa la relación entre torneos y juegos. Muestra qué juegos pertenecen a qué torneos.

- **`TorneoParticipanteSerializer`**:  
  Serializa la relación entre torneos y participantes. Muestra qué participantes están inscritos en cada torneo.

- **`TorneoJugadorSerializer`**:  
  Serializa la relación entre torneos y jugadores. Muestra qué jugadores participan en qué torneos.

---

## 🚀 **Vistas y Endpoints**  
La API proporciona diferentes **vistas** que permiten consultar la base de datos de forma sencilla o mejorada. Estas vistas están disponibles como endpoints que devuelven datos en formato JSON.

### **Consultas sencillas**:

- **`torneo_list_sencillo`**:  
  Endpoint: `/api/v1/torneos/`  
  Devuelve una lista de torneos sin optimizaciones adicionales. Utiliza el `TorneoSerializer`.

- **`equipo_list_sencillo`**:  
  Endpoint: `/api/v1/equipos/`  
  Devuelve una lista de equipos sin optimización, utilizando el `EquipoSerializer`.

### **Consultas mejoradas**:

- **`torneo_list`**:  
  Endpoint: `/api/v1/torneos/mejorada/`  
  Devuelve una lista de torneos con optimizaciones como `prefetch_related` para reducir consultas adicionales. Utiliza el `TorneoSerializerMejorado`, que incluye participantes y juegos asociados al torneo.

- **`participante_list_mejorado`**:  
  Endpoint: `/api/v1/participantes/mejorada/`  
  Devuelve una lista de participantes mejorada. Incluye información sobre el usuario, equipos y torneos asociados. Usa el `ParticipanteSerializerMejorado`.

- **`juego_list_mejorado`**:  
  Endpoint: `/api/v1/juegos/mejorada/`  
  Devuelve una lista de juegos con optimizaciones. Incluye detalles sobre los torneos y las consolas asociadas a cada juego. Usa el `JuegoSerializerMejorado`.

---

## ⚡ **Optimización y Mejora de Consultas**  
En algunas vistas se han implementado optimizaciones de rendimiento utilizando `prefetch_related` para reducir el número de consultas a la base de datos, especialmente en relaciones **ManyToMany** o **ForeignKey**.

- **`prefetch_related`**:  
  Se utiliza para hacer una única consulta a la base de datos por cada relación que se necesita cargar. Esto es útil cuando tenemos relaciones como la de participantes en un torneo o los juegos en un torneo.

Por ejemplo, en la vista `torneo_list` se prefetchan las relaciones `participantes` y `juegos_torneo`, lo que reduce el número de consultas realizadas al acceder a los torneos y sus detalles.

---

## 🛠 **URLs**  
A continuación se encuentran las rutas definidas en la API para acceder a los datos:

- **`/api/v1/torneos/`**: Listado de torneos (consulta sencilla).
- **`/api/v1/torneos/mejorada/`**: Listado de torneos con detalles mejorados (optimización).
- **`/api/v1/equipos/`**: Listado de equipos (consulta sencilla).
- **`/api/v1/equipos/mejorada/`**: Listado de equipos con detalles mejorados.
- **`/api/v1/participantes/mejorada/`**: Listado de participantes con detalles mejorados.
- **`/api/v1/juegos/mejorada/`**: Listado de juegos con detalles mejorados.

---

## 🔒 **Autenticación y Permisos**  
La API utiliza **JWT (JSON Web Token)** para la autenticación. Puedes obtener un token mediante el endpoint `/api/v1/token/` y usarlo para realizar peticiones autenticadas.

---
## 💻 **Realizar Peticiones desde el Cliente**  
Puedes hacer peticiones a los endpoints de la API desde cualquier cliente HTTP, como **Postman**, **Insomnia** o directamente desde tu aplicación frontend.











