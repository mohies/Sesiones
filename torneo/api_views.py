from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import status
from .forms import *
from django.db.models import Q, Prefetch
from django.contrib.auth.models import Group
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated

#Crear una consulta sencilla al listado de vuestro modelo principal de la aplicación y mostrarla en vuestra aplicación cliente. (1 punto)
@api_view(['GET'])
def torneo_list_sencillo(request):
    # Obtener todos los torneos sin optimizaciones adicionales
    torneos = Torneo.objects.all()

    # Serializar los torneos usando un serializer básico
    serializer = TorneoSerializer(torneos, many=True)

    # Devuelve los datos serializados
    return Response(serializer.data)

#Crear una consulta mejorada al listado de vuestro modelo principal de la aplicación cliente. Debe ser una vista distinta a la anterior, con un template y url disntinta. (1 punto
@api_view(['GET'])
def torneo_list(request):
    # Usamos prefetch_related con el related_name 'participante_torneo' o 'torneoparticipante_set' dependiendo de cómo lo hayas configurado
    torneos = Torneo.objects.prefetch_related('torneoparticipante_set').all()
    serializer = TorneoSerializerMejorado(torneos, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def equipo_list_sencillo(request):
    # Obtener todos los equipos
    equipos = Equipo.objects.all()
    
    # Serializar los equipos usando el serializer mejorado
    serializer = EquipoSerializerMejorado(equipos, many=True)
    
    # Devuelve los datos serializados
    return Response(serializer.data)

@api_view(['GET'])
def participante_list_mejorado(request):
    # Optimizar relaciones ManyToMany con prefetch_related usando el related_name 'participante_torneo'
    participantes = Participante.objects.prefetch_related('participanteequipo_set').all()
    
    # Serializar con el serializer mejorado
    serializer = ParticipanteSerializerMejorado(participantes, many=True)
    
    # Devolver los datos serializados
    return Response(serializer.data)




@api_view(['GET'])
def juego_list_mejorado(request):
    juegos = Juego.objects.prefetch_related('torneos').all()  # Prefetch de la relación ManyToMany
    
    # Serializa los juegos usando el serializador correspondiente
    serializer = JuegoSerializerMejorado(juegos, many=True)
    
    # Devuelve los datos serializados
    return Response(serializer.data)