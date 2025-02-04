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


@api_view(['GET'])
def torneo_buscar(request):
    formulario = BusquedaTorneoForm(request.query_params)
    if formulario.is_valid():
        texto = formulario.data.get('textoBusqueda')
        torneos = Torneo.objects.prefetch_related("participantes","juegos_torneo")
        torneos = torneos.filter(Q(nombre__contains=texto) | Q(descripcion__contains=texto)).all()
        serializer = TorneoSerializerMejorado(torneos, many=True)
        return Response(serializer.data)
    else:
        return Response(formulario.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def torneo_buscar_avanzado(request):
    if len(request.query_params) > 0:
        formulario = BusquedaAvanzadaTorneoForm(request.query_params)
        if formulario.is_valid():
            QStorneos = Torneo.objects.prefetch_related("participantes")

            textoBusqueda = formulario.cleaned_data.get('textoBusqueda')
            fechaDesde = formulario.cleaned_data.get('fecha_desde')
            fechaHasta = formulario.cleaned_data.get('fecha_hasta')
            categoria = formulario.cleaned_data.get('categoria')

            if textoBusqueda:
                QStorneos = QStorneos.filter(Q(nombre__icontains=textoBusqueda) | Q(descripcion__icontains=textoBusqueda) | Q(categoria__contains=textoBusqueda))

            if fechaDesde:
                QStorneos = QStorneos.filter(fecha_inicio__gte=fechaDesde)

            if fechaHasta:
                QStorneos = QStorneos.filter(fecha_inicio__lte=fechaHasta)

            if categoria:
                QStorneos = QStorneos.filter(categoria__icontains=categoria)

            torneos = QStorneos.all()
            serializer = TorneoSerializerMejorado(torneos, many=True)
            return Response(serializer.data)
        else:
            return Response(formulario.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def equipo_buscar_avanzado(request):
    if len(request.query_params) > 0:
        formulario = BusquedaAvanzadaEquipoForm(request.query_params)
        if formulario.is_valid():
            QEquipos = Equipo.objects.all()

            nombre = formulario.cleaned_data.get('nombre')
            fechaIngresoDesde = formulario.cleaned_data.get('fecha_ingreso_desde')
            fechaIngresoHasta = formulario.cleaned_data.get('fecha_ingreso_hasta')
            puntosContribuidosMin = formulario.cleaned_data.get('puntos_contribuidos_min')

            if nombre:
                QEquipos = QEquipos.filter(nombre__icontains=nombre)

            if fechaIngresoDesde:
                QEquipos = QEquipos.filter(fecha_ingreso__gte=fechaIngresoDesde)

            if fechaIngresoHasta:
                QEquipos = QEquipos.filter(fecha_ingreso__lte=fechaIngresoHasta)

            if puntosContribuidosMin:
                QEquipos = QEquipos.filter(puntos_contribuidos__gte=puntosContribuidosMin)

            equipos = QEquipos.all()
            serializer = EquipoSerializerMejorado(equipos, many=True)
            return Response(serializer.data)
        else:
            return Response(formulario.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': 'No se proporcionaron parámetros de búsqueda.'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def participante_buscar_avanzado(request):
    if len(request.query_params) > 0:
        formulario = BusquedaAvanzadaParticipanteForm(request.query_params)
        if formulario.is_valid():
            QParticipantes = Participante.objects.prefetch_related('equipos')

            nombre = formulario.cleaned_data.get('nombre')
            puntosObtenidosMin = formulario.cleaned_data.get('puntos_obtenidos_min')
            fechaInscripcionDesde = formulario.cleaned_data.get('fecha_inscripcion_desde')
            fechaInscripcionHasta = formulario.cleaned_data.get('fecha_inscripcion_hasta')

            if nombre:
                QParticipantes = QParticipantes.filter(usuario__nombre__icontains=nombre)

            if puntosObtenidosMin:
                QParticipantes = QParticipantes.filter(puntos_obtenidos__gte=puntosObtenidosMin)

            if fechaInscripcionDesde:
                QParticipantes = QParticipantes.filter(fecha_inscripcion__gte=fechaInscripcionDesde)

            if fechaInscripcionHasta:
                QParticipantes = QParticipantes.filter(fecha_inscripcion__lte=fechaInscripcionHasta)

            participantes = QParticipantes.all()
            serializer = ParticipanteSerializerMejorado(participantes, many=True)
            return Response(serializer.data)
        else:
            return Response(formulario.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': 'No se proporcionaron parámetros de búsqueda.'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def juego_buscar_avanzado(request):
    if len(request.query_params) > 0:
        formulario = BusquedaAvanzadaJuegoForm(request.query_params)
        if formulario.is_valid():
            QJuegos = Juego.objects.prefetch_related('torneos')

            nombre = formulario.cleaned_data.get('nombre')
            genero = formulario.cleaned_data.get('genero')
            fechaParticipacionDesde = formulario.cleaned_data.get('fecha_participacion_desde')
            fechaParticipacionHasta = formulario.cleaned_data.get('fecha_participacion_hasta')

            if nombre:
                QJuegos = QJuegos.filter(nombre__icontains=nombre)

            if genero:
                QJuegos = QJuegos.filter(genero__icontains=genero)

            if fechaParticipacionDesde:
                QJuegos = QJuegos.filter(torneojuego__fecha_participacion__gte=fechaParticipacionDesde)

            if fechaParticipacionHasta:
                QJuegos = QJuegos.filter(torneojuego__fecha_participacion__lte=fechaParticipacionHasta)

            juegos = QJuegos.all()
            serializer = JuegoSerializerMejorado(juegos, many=True)
            return Response(serializer.data)
        else:
            return Response(formulario.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': 'No se proporcionaron parámetros de búsqueda.'}, status=status.HTTP_400_BAD_REQUEST)

