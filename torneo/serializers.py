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
    participantes = ParticipanteSerializer(many=True, read_only=True)
    jugadores = JugadorSerializer(many=True, read_only=True)  # 🔹 Agregado para incluir jugadores
    fecha_inicio = serializers.DateField(format='%d-%m-%Y')
    categoria = serializers.CharField()

    class Meta:
        model = Torneo
        fields = ('id', 'nombre', 'descripcion', 'categoria', 'duracion', 'fecha_inicio', 'participantes','jugadores')
        
        
class EquipoSerializerMejorado(serializers.ModelSerializer):
    class Meta:
        model = Equipo
        fecha_ingreso = serializers.DateField(format='%d-%m-%Y')
        fields = ('id', 'nombre', 'logotipo', 'puntos_contribuidos','fecha_ingreso')  # Usamos puntos_contribuidos directamente
        
        


class ParticipanteSerializerMejorado(serializers.ModelSerializer):
    usuario = serializers.PrimaryKeyRelatedField(queryset=Usuario.objects.all())  # 🔹 Esto asegura que 'usuario' esté presente
    nombre_usuario = serializers.CharField(source='usuario.nombre', read_only=True)
    equipos = EquipoSerializer(many=True, read_only=True)  
    torneos = TorneoSerializer(many=True, read_only=True)  

    class Meta:
        model = Participante
        fields = ['id', 'usuario', 'nombre_usuario', 'puntos_obtenidos', 'posicion_final', 'fecha_inscripcion', 'tiempo_jugado', 'equipos', 'torneos']


        
class JuegoSerializerMejorado(serializers.ModelSerializer):
    consola = serializers.CharField(source='id_consola.nombre')  # Mostrar el nombre de la consola
    torneos = TorneoSerializer(many=True)  # Relación con los torneos

    class Meta:
        model = Juego
        fields = ['id', 'nombre', 'genero', 'descripcion','id_consola', 'consola','torneo', 'torneos']
        
import base64
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile       
class TorneoSerializerCreate(serializers.ModelSerializer):
    imagen = serializers.CharField(required=False, allow_null=True)  # Se usa base64 como string

    class Meta:
        model = Torneo
        fields = ['nombre', 'descripcion', 'fecha_inicio', 
                  'categoria', 'duracion', 'imagen']  # Incluir la imagen como campo

    def create(self, validated_data):
        # Verificar si se ha recibido la imagen en base64
        imagen_base64 = self.initial_data.get('imagen', None)
        if imagen_base64:
            # Decodificar la imagen en base64
            imagen = base64.b64decode(imagen_base64)
            contenido_archivo = ContentFile(imagen)

            # Crear el archivo InMemoryUploadedFile
            archivo = InMemoryUploadedFile(
                contenido_archivo,       
                None,                
                'imagen_torneo',  # Nombre ficticio para la imagen
                'image/jpeg',  # Tipo MIME
                len(imagen),        
                None
            )
            validated_data["imagen"] = archivo  # Asignar el archivo al campo imagen

        # Crear el torneo con la imagen (si la hay)
        torneo = Torneo.objects.create(
            nombre=validated_data["nombre"],
            descripcion=validated_data["descripcion"],
            fecha_inicio=validated_data["fecha_inicio"],
            categoria=validated_data["categoria"],
            duracion=validated_data["duracion"],
            imagen=validated_data.get("imagen")  # Guardar la imagen si está presente
        )

        return torneo

    def update(self, instance, validated_data):
        # Verificar si se ha recibido la imagen en base64
        imagen_base64 = self.initial_data.get('imagen', None)
        if imagen_base64:
            # Decodificar la imagen en base64
            imagen = base64.b64decode(imagen_base64)
            contenido_archivo = ContentFile(imagen)

            # Crear el archivo InMemoryUploadedFile
            archivo = InMemoryUploadedFile(
                contenido_archivo,       
                None,                
                'imagen_torneo',  # Nombre ficticio para la imagen
                'image/jpeg',  # Tipo MIME
                len(imagen),        
                None
            )
            instance.imagen = archivo  # Asignar el archivo al campo imagen

        # Actualizar los datos del torneo con la nueva imagen (si está presente)
        instance.nombre = validated_data.get("nombre", instance.nombre)
        instance.descripcion = validated_data.get("descripcion", instance.descripcion)
        instance.fecha_inicio = validated_data.get("fecha_inicio", instance.fecha_inicio)
        instance.categoria = validated_data.get("categoria", instance.categoria)
        instance.duracion = validated_data.get("duracion", instance.duracion)
        instance.save()

        return instance
    
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

    #  Validación 1: El nombre del juego no debe repetirse en el mismo torneo
    def validate_nombre(self, nombre):
        juego_existente = Juego.objects.filter(nombre=nombre).first()
        if juego_existente:
            if self.instance and juego_existente.id == self.instance.id:
                pass  # Permite actualizar el mismo juego sin error
            else:
                raise serializers.ValidationError("Ya existe un juego con ese nombre en este torneo.")
        return nombre

    # Validación 2: La descripción debe tener al menos 10 caracteres
    def validate_descripcion(self, descripcion):
        if len(descripcion) < 10:
            raise serializers.ValidationError("Al menos debes indicar 10 caracteres en la descripción.")
        return descripcion

    #  Validación 3: El género del juego no puede estar vacío
    def validate_genero(self, genero):
        if genero == "":
            raise serializers.ValidationError("Debes seleccionar un género.")
        return genero
    


class JuegoSerializerActualizarNombre(serializers.ModelSerializer):
    class Meta:
        model = Juego
        fields = ['nombre']

    def validate_nombre(self, nombre):
        """
        Validación: No permitir nombres duplicados en la misma consola.
        """
        juego_existente = Juego.objects.filter(nombre=nombre).first()
        if juego_existente and juego_existente.id != self.instance.id:
            raise serializers.ValidationError("Ya existe un juego con ese nombre.")
        return nombre




class ParticipanteSerializerCreate(serializers.ModelSerializer):

    # Lista de equipos disponibles para seleccionar en el formulario
    equipos = serializers.PrimaryKeyRelatedField(queryset=Equipo.objects.all(), many=True)

    class Meta:
        model = Participante
        fields = ['usuario', 'puntos_obtenidos', 'posicion_final', 'fecha_inscripcion', 'tiempo_jugado', 'equipos']

    # Validación 1: Un participante no puede inscribirse dos veces con el mismo usuario
    def validate_usuario(self, usuario):
        participante_existente = Participante.objects.filter(usuario=usuario).first()
        if participante_existente and participante_existente.id != self.instance.id:
            raise serializers.ValidationError("Este usuario ya está registrado como participante.")
        return usuario

    # Validación 2: Los puntos obtenidos no pueden ser negativos
    def validate_puntos_obtenidos(self, puntos):
        if puntos < 0:
            raise serializers.ValidationError("Los puntos obtenidos no pueden ser negativos.")
        return puntos

    # Validación 3: El participante debe pertenecer al menos a un equipo
    def validate_equipos(self, equipos):
        if len(equipos) < 1:
            raise serializers.ValidationError("Debe seleccionar al menos un equipo.")
        return equipos




class ParticipanteSerializerActualizarEquipos(serializers.ModelSerializer):
    equipos = serializers.PrimaryKeyRelatedField(queryset=Equipo.objects.all(), many=True)  # Selección de varios equipos

    class Meta:
        model = Participante
        fields = ['equipos']

    def validate_equipos(self, equipos):
        """
        Validación: Asegurar que los equipos seleccionados existen.
        """
        if not equipos:
            raise serializers.ValidationError("Debes seleccionar al menos un equipo.")
        return equipos



class JugadorSerializerCreate(serializers.ModelSerializer):
    
    class Meta:
        model = Jugador
        fields = ['usuario', 'puntos', 'equipo', 'torneos']  # Campos requeridos

    def validate_usuario(self, usuario):
        """
        Valida que el usuario no esté duplicado en la base de datos.
        """
        jugador_existente = Jugador.objects.filter(usuario=usuario).first()
        if jugador_existente and (self.instance is None or jugador_existente.id != self.instance.id):
            raise serializers.ValidationError("Ya existe un jugador con este usuario.")
        return usuario

    def validate_puntos(self, puntos):
        """
        Valida que los puntos no sean negativos.
        """
        if puntos < 0:
            raise serializers.ValidationError("Los puntos no pueden ser negativos.")
        return puntos

    def validate_torneos(self, torneos):
        """
        Valida que todos los torneos en la lista existan en la base de datos.
        """
        if len(torneos) < 1:
            raise serializers.ValidationError("Debe seleccionar al menos un torneo.")
        
        for torneo_id in torneos:
            if not Torneo.objects.filter(id=torneo_id).exists():
                raise serializers.ValidationError(f"El torneo con ID {torneo_id} no existe.")
        
        return torneos

    def create(self, validated_data):
        """
        Crea un nuevo jugador y asocia los torneos seleccionados.
        """
        torneos = self.initial_data['torneos']

        # Crear el jugador
        jugador = Jugador.objects.create(
            usuario=validated_data["usuario"],
            puntos=validated_data["puntos"],
            equipo=validated_data["equipo"]
        )

        # Asociar torneos con el jugador
        for torneo_id in torneos:
            torneo = Torneo.objects.get(id=torneo_id)
            TorneoJugador.objects.create(torneo=torneo, jugador=jugador)

        return jugador

    def update(self, instance, validated_data):
        """
        Actualiza un jugador y sus torneos asociados.
        """
        torneos = self.initial_data['torneos']

        # Validación: Un jugador debe estar en al menos un torneo
        if len(torneos) < 1:
            raise serializers.ValidationError(
                {"torneos": ["Debe seleccionar al menos un torneo."]}
            )

        # Actualizar los campos básicos del jugador
        instance.puntos = validated_data["puntos"]
        instance.equipo = validated_data["equipo"]
        instance.save()

        # Actualizar la relación ManyToMany con `through`
        instance.torneos.clear()  # Elimina las relaciones actuales

        for torneo_id in torneos:
            torneo = Torneo.objects.get(id=torneo_id)
            TorneoJugador.objects.create(torneo=torneo, jugador=instance)  # Crea la relación

        return instance


    
    
class JugadorActualizarPuntosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jugador
        fields = ['puntos']

    def validate_puntos(self, puntos):
        """
        Validación: Los puntos no pueden ser negativos.
        """
        if puntos < 0:
            raise serializers.ValidationError("Los puntos no pueden ser negativos.")
        return puntos
