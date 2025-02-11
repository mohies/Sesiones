from rest_framework import serializers
from .models import UsuarioLogin, Organizador, Usuario, PerfilDeJugador, Equipo, Participante, Torneo, Jugador, Consola, Juego, Espectador, Clasificacion, ParticipanteEquipo, TorneoJuego, TorneoParticipante, TorneoJugador

class UsuarioLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsuarioLogin
        fields = '__all__'


class OrganizadorSerializer(serializers.ModelSerializer):
    usuario = UsuarioLoginSerializer()

    class Meta:
        model = Organizador
        fields = '__all__'


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'


class PerfilDeJugadorSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer()

    class Meta:
        model = PerfilDeJugador
        fields = '__all__'


class EquipoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipo
        fields = '__all__'


class ParticipanteSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer()
    equipos = EquipoSerializer(many=True)

    class Meta:
        model = Participante
        fields = '__all__'

#Crear una consulta sencilla al listado de vuestro modelo principal de la aplicación y mostrarla en vuestra aplicación cliente. (1 punto)
class TorneoSerializer(serializers.ModelSerializer):
    participantes = ParticipanteSerializer(many=True)

    class Meta:
        model = Torneo
        fields = '__all__'


class JugadorSerializer(serializers.ModelSerializer):
    usuario = UsuarioLoginSerializer()
    torneos = TorneoSerializer(many=True)

    class Meta:
        model = Jugador
        fields = '__all__'


class ConsolaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consola
        fields = '__all__'


class JuegoSerializer(serializers.ModelSerializer):
    torneo = TorneoSerializer()
    id_consola = ConsolaSerializer()

    class Meta:
        model = Juego
        fields = '__all__'


class EspectadorSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer()

    class Meta:
        model = Espectador
        fields = '__all__'


class ClasificacionSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer()

    class Meta:
        model = Clasificacion
        fields = '__all__'


class ParticipanteEquipoSerializer(serializers.ModelSerializer):
    participante = ParticipanteSerializer()
    equipo = EquipoSerializer()

    class Meta:
        model = ParticipanteEquipo
        fields = '__all__'


class TorneoJuegoSerializer(serializers.ModelSerializer):
    torneo = TorneoSerializer()
    juego = JuegoSerializer()

    class Meta:
        model = TorneoJuego
        fields = '__all__'


class TorneoParticipanteSerializer(serializers.ModelSerializer):
    torneo = TorneoSerializer()
    participante = ParticipanteSerializer()

    class Meta:
        model = TorneoParticipante
        fields = '__all__'


class TorneoJugadorSerializer(serializers.ModelSerializer):
    torneo = TorneoSerializer()
    jugador = JugadorSerializer()

    class Meta:
        model = TorneoJugador
        fields = '__all__'
#Crear una consulta mejorada al listado de vuestro modelo principal de la aplicación cliente. Debe ser una vista distinta a la anterior, con un template y url disntinta. (1 punto     
class TorneoSerializerMejorado(serializers.ModelSerializer):
    participantes = ParticipanteSerializer(many=True)

    fecha_inicio = serializers.DateField(format='%d-%m-%Y')
    categoria = serializers.CharField()

    class Meta:
        model = Torneo
        fields = ('id', 'nombre', 'descripcion', 'categoria', 'duracion', 'fecha_inicio', 'participantes')
        
        
class EquipoSerializerMejorado(serializers.ModelSerializer):
    class Meta:
        model = Equipo
        fecha_ingreso = serializers.DateField(format='%d-%m-%Y')
        fields = ('id', 'nombre', 'logotipo', 'puntos_contribuidos','fecha_ingreso')  # Usamos puntos_contribuidos directamente
        
        


class ParticipanteSerializerMejorado(serializers.ModelSerializer):
    nombre_usuario = serializers.CharField(source='usuario.nombre')
    equipos = EquipoSerializer(many=True, read_only=True)  # Usamos el EquipoSerializer para mostrar los detalles del equipo
    torneos = TorneoSerializer(many=True, read_only=True)  # Usamos el TorneoSerializer para mostrar los detalles del torneo

    class Meta:
        model = Participante
        fields = ['nombre_usuario', 'puntos_obtenidos', 'posicion_final', 'fecha_inscripcion', 'tiempo_jugado', 'equipos', 'torneos']

        
class JuegoSerializerMejorado(serializers.ModelSerializer):
    consola = serializers.CharField(source='id_consola.nombre')  # Mostrar el nombre de la consola
    torneos = TorneoSerializer(many=True)  # Relación con los torneos

    class Meta:
        model = Juego
        fields = ['id', 'nombre', 'genero', 'descripcion','id_consola', 'consola','torneo', 'torneos']
        
        
class TorneoSerializerCreate(serializers.ModelSerializer):
    
    class Meta:
        model = Torneo
        fields = ['nombre', 'descripcion', 'fecha_inicio', 
                  'categoria', 'duracion', 'participantes']

    def validate_nombre(self, value):
        """Verifica que el nombre del torneo no exista en la base de datos"""
        if Torneo.objects.filter(nombre=value).exists():
            raise serializers.ValidationError("Ya existe un torneo con este nombre.")
        if len(value) < 5:
            raise serializers.ValidationError("El nombre debe tener al menos 5 caracteres.")
        return value  # Siempre devolvemos el valor validado

    def validate_fecha_inicio(self, value):
        """La fecha de inicio no puede ser en el pasado"""
        from datetime import date
        if value < date.today():
            raise serializers.ValidationError("La fecha de inicio no puede ser en el pasado.")
        return value

    def validate_duracion(self, value):
        """La duración no puede ser menor a 1 hora"""
        from datetime import timedelta
        if value < timedelta(hours=1):
            raise serializers.ValidationError("La duración mínima debe ser de 1 hora.")
        return value
    
class TorneoSerializerActualizarNombre(serializers.ModelSerializer):
    class Meta:
        model = Torneo
        fields = ['nombre']
        
    def validate_nombre(self, nombre):
        """
        Valida que el nombre del torneo no esté repetido.
        """
        torneo_existente = Torneo.objects.filter(nombre=nombre).first()
        if torneo_existente and torneo_existente.id != self.instance.id:
            raise serializers.ValidationError('Ya existe un torneo con ese nombre')
        return nombre  #  Si no hay problema, devuelve el nombre original
    
class JuegoSerializerCreate(serializers.ModelSerializer):
    
    GENEROS_CHOICES = [
        ("", "Selecciona un género"),  # Opción vacía por defecto
        ("Acción", "Acción"),
        ("Aventura", "Aventura"),
        ("Estrategia", "Estrategia"),
        ("Deportes", "Deportes"),
        ("RPG", "RPG"),
        ("Shooter", "Shooter"),
    ]

    torneo = serializers.PrimaryKeyRelatedField(queryset=Torneo.objects.all())  # Torneo obligatorio
    id_consola = serializers.PrimaryKeyRelatedField(queryset=Consola.objects.all())  # Consola obligatoria
    genero = serializers.ChoiceField(choices=GENEROS_CHOICES)  # Género ahora es un ChoiceField

    class Meta:
        model = Juego
        fields = ['torneo', 'nombre', 'genero', 'id_consola', 'descripcion']

    # 🔹 Validación 1: El nombre del juego no debe repetirse en el mismo torneo
    def validate_nombre(self, nombre):
        juego_existente = Juego.objects.filter(nombre=nombre).first()
        if juego_existente:
            if self.instance and juego_existente.id == self.instance.id:
                pass  # Permite actualizar el mismo juego sin error
            else:
                raise serializers.ValidationError("Ya existe un juego con ese nombre en este torneo.")
        return nombre

    # 🔹 Validación 2: La descripción debe tener al menos 10 caracteres
    def validate_descripcion(self, descripcion):
        if len(descripcion) < 10:
            raise serializers.ValidationError("Al menos debes indicar 10 caracteres en la descripción.")
        return descripcion

    # 🔹 Validación 3: El género del juego no puede estar vacío
    def validate_genero(self, genero):
        if genero == "":
            raise serializers.ValidationError("Debes seleccionar un género.")
        return genero

