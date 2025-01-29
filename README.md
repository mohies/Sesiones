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




