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

@api_view(['GET'])
def participante_list(request):
    participantes = Participante.objects.all()
    serializer = ParticipanteSerializer(participantes, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def categoria_list(request):
    """
    Devuelve una lista de categorías disponibles en los torneos.
    """
    categorias = Torneo.objects.values_list('categoria', flat=True).distinct()
    return Response(list(categorias))


@api_view(['POST'])
def torneo_create(request): 
    print(request.data)  # Para depuración
    torneoCreateSerializer = TorneoSerializerCreate(data=request.data)

    if torneoCreateSerializer.is_valid():
        try:
            torneoCreateSerializer.save()
            return Response("Torneo CREADO")
        except serializers.ValidationError as error:
            return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            print(repr(error))
            return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(torneoCreateSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    
@api_view(['GET']) 
def torneo_obtener(request, torneo_id):
    """
    Obtiene un torneo específico con sus relaciones (participantes y otros datos).
    """
    torneo = Torneo.objects.prefetch_related("participantes").get(id=torneo_id)
    serializer = TorneoSerializerMejorado(torneo)  # 🔹 Usamos un serializer mejorado
    return Response(serializer.data)



@api_view(['PUT'])
def torneo_editar(request, torneo_id):
    torneo = Torneo.objects.get(id=torneo_id)
    torneoCreateSerializer = TorneoSerializerCreate(data=request.data, instance=torneo)
    
    if torneoCreateSerializer.is_valid():
        try:
            torneoCreateSerializer.save()
            return Response("Torneo EDITADO")
        except serializers.ValidationError as error:
            return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(torneoCreateSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
@api_view(['PATCH'])
def torneo_actualizar_nombre(request, torneo_id):
    """
    Actualiza solo el nombre de un torneo específico.
    """
    torneo = Torneo.objects.get(id=torneo_id)
    serializer = TorneoSerializerActualizarNombre(data=request.data, instance=torneo)

    if serializer.is_valid():
        try:
            serializer.save()
            return Response("Torneo EDITADO")
        except Exception as error:
            print(repr(error))
            return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
@api_view(['DELETE'])
def torneo_eliminar(request, torneo_id):
    torneo = Torneo.objects.get(id=torneo_id)  # 🔹 Obtiene el torneo
    try:
        torneo.delete()
        return Response("Torneo ELIMINADO")  # ✅ Mensaje igual al del profesor
    except Exception as error:
        return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def torneo_list(request):
    """
    Devuelve la lista de todos los torneos registrados.
    """
    torneos = Torneo.objects.all()  # Obtiene todos los torneos
    serializer = TorneoSerializer(torneos, many=True)  # ✅ Serializa los torneos
    return Response(serializer.data)  # Retorna la respuesta en JSON

@api_view(['GET'])
def consola_list(request):
    """
    Devuelve la lista de todas las consolas registradas.
    """
    consolas = Consola.objects.all()  # Obtiene todas las consolas
    serializer = ConsolaSerializer(consolas, many=True)  # Serializa las consolas
    return Response(serializer.data)  # Retorna la respuesta en JSON



@api_view(['POST'])
def juego_create(request): 
    print(request.data)  # Para depuración
    juegoCreateSerializer = JuegoSerializerCreate(data=request.data)

    if juegoCreateSerializer.is_valid():
        try:
            juegoCreateSerializer.save()
            return Response("Juego CREADO")
        except serializers.ValidationError as error:
            return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            print(repr(error))
            return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(juegoCreateSerializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET']) 
def juego_obtener(request, juego_id):
    """
    Obtiene un juego específico con sus relaciones (torneo y consola).
    """
    juego = Juego.objects.select_related("torneo", "id_consola").get(id=juego_id)
    serializer = JuegoSerializerMejorado(juego)  # 🔹 Usamos un serializer mejorado
    return Response(serializer.data)



@api_view(['PUT'])
def juego_editar(request, juego_id):
    """
    Editar un juego específico con los datos proporcionados.
    """
    juego = Juego.objects.get(id=juego_id)
    juegoCreateSerializer = JuegoSerializerCreate(data=request.data, instance=juego)

    if juegoCreateSerializer.is_valid():
        try:
            juegoCreateSerializer.save()
            return Response("Juego EDITADO")
        except serializers.ValidationError as error:
            return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(juegoCreateSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

