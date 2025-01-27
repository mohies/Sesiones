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
    # Relaciones ManyToMany a través de otros serializers
    participantes = ParticipanteSerializer(many=True)
    juegos = JuegoSerializer(many=True, source='juegos_torneo')  # Usamos 'juegos_torneo' que es el related_name en el modelo Juego

    # Para formatear la fecha de inicio
    fecha_inicio = serializers.DateField(format='%d-%m-%Y')

    # Para obtener el nombre de la categoría, no necesitas 'get_categoria_display', ya que no está definida en el modelo
    categoria = serializers.CharField()

    class Meta:
        model = Torneo
        fields = ('id', 'nombre', 'descripcion', 'categoria', 'duracion', 'fecha_inicio', 'participantes', 'juegos')
        
        
class EquipoSerializerMejorado(serializers.ModelSerializer):
    class Meta:
        model = Equipo
        fields = ('id', 'nombre', 'logotipo', 'puntos_contribuidos')  # Usamos puntos_contribuidos directamente
        
        


class ParticipanteSerializerMejorado(serializers.ModelSerializer):
    # Agregamos un campo adicional para el nombre del usuario
    nombre_usuario = serializers.CharField(source='usuario.nombre', read_only=True)
    
    # Campo torneos usando el related_name y accediendo a los torneos del participante
    torneos = serializers.PrimaryKeyRelatedField(queryset=Torneo.objects.all(), many=True, source='participante_torneo.all')

    class Meta:
        model = Participante
        fields = ['nombre_usuario', 'puntos_obtenidos', 'posicion_final', 'fecha_inscripcion', 'tiempo_jugado', 'equipos', 'torneos']
        
class JuegoSerializerMejorado(serializers.ModelSerializer):
    consola = serializers.StringRelatedField()  # Muestra el nombre de la consola
    torneos = TorneoSerializer(many=True)  # Relación con los torneos

    class Meta:
        model = Juego
        fields = ['id', 'nombre', 'genero', 'descripcion', 'consola', 'torneos']
