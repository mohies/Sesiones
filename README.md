# Proyecto de Aplicación Web de Torneos de Videojuegos

## Validaciones Implementadas

### 1. TorneoForm
- **nombre**: Verifica que no exista otro torneo con el mismo nombre en la base de datos. Si ya existe, muestra un error.
- **descripcion**: Valida que tenga al menos 20 caracteres.
- **fecha_inicio**: No puede ser una fecha anterior al día actual.
- **categoria**: Si la categoría es "Acción", la duración del torneo no puede superar las 3 horas.
- **participantes**: Deben seleccionarse al menos 2 participantes.

### 2. BusquedaTorneoForm
- **textoBusqueda**: Valida que el texto de búsqueda tenga al menos 3 caracteres.

### 3. BusquedaAvanzadaTorneoForm
- **Campos**: Valida que al menos uno de los campos esté completo.
- **fecha_desde y fecha_hasta**: Valida que la fecha "hasta" no sea anterior a la fecha "desde".
- **duracion_minima**: Debe ser un tiempo válido y mayor que cero.

### 4. EquipoForm
- **nombre**: Verifica que no exista otro equipo con el mismo nombre en la base de datos.
- **logotipo**: Si se proporciona, debe ser una URL válida.
- **fecha_ingreso**: No puede ser una fecha futura ni menor al día actual.
- **puntos_contribuidos**: Debe ser un valor positivo.

### 5. BusquedaAvanzadaEquipoForm
- **Campos**: Valida que al menos uno de los campos esté completo.
- **fecha_ingreso_desde y fecha_ingreso_hasta**: Valida que la fecha "hasta" no sea anterior a la fecha "desde".
- **puntos_minimos y puntos_maximos**: Los puntos mínimos no pueden ser mayores que los máximos.

### 6. ParticipanteForm
- **usuario**: Verifica que el usuario no esté registrado como participante.
- **puntos_obtenidos**: Debe ser un valor positivo.
- **posicion_final**: Debe ser un número positivo.
- **tiempo_jugado**: No puede ser negativo.
- **equipos**: Debe seleccionarse al menos un equipo.

### 7. BusquedaAvanzadaParticipanteForm
- **Campos**: Valida que al menos uno de los campos esté completo.
- **fecha_inscripcion_desde y fecha_inscripcion_hasta**: Valida que la fecha "hasta" no sea anterior a la fecha "desde".
- **puntos_minimos y puntos_maximos**: Los puntos mínimos no pueden ser mayores que los máximos.
- **tiempo_jugado_minimo y tiempo_jugado_maximo**: El tiempo jugado mínimo no puede ser mayor que el máximo.

### 8. UsuarioForm
- **correo**: Verifica que no exista otro usuario con el mismo correo en la base de datos.
- **nombre**: Verifica que no exista otro usuario con el mismo nombre.
- **clave_de_acceso**: Debe tener al menos 8 caracteres.

### 9. BusquedaUsuarioForm
- **Campos**: Valida que al menos uno de los campos esté completo.
- **fecha_registro_desde y fecha_registro_hasta**: Valida que la fecha "hasta" no sea anterior a la fecha "desde".

### 10. JuegoForm
- **nombre**: Verifica que no exista otro juego con el mismo nombre en la base de datos.

### 11. BusquedaJuegoForm
- **Campos**: Valida que al menos tres de los campos estén completos.

### 12. PerfilDeJugadorForm
- **usuario**: Verifica que no exista otro perfil de jugador asociado al mismo usuario.
- **puntos, nivel y ranking**: Deben ser valores positivos.
- **avatar**: Si se proporciona, debe ser una URL válida.

### 13. BusquedaAvanzadaPerfilJugadorForm
- **Campos**: Valida que al menos uno de los campos esté completo.
- **textoBusqueda**: Si se proporciona, debe tener al menos 3 caracteres.
- **puntos_minimos y nivel_minimo**: Deben ser valores positivos.
