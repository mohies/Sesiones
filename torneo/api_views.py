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
import logging
from django.shortcuts import redirect

logger = logging.getLogger(__name__)

def handle_error(request, error_message, status_code):
    logger.error(error_message)
    if status_code == status.HTTP_404_NOT_FOUND:
        return redirect('/error/404')
    elif status_code == status.HTTP_400_BAD_REQUEST:
        return redirect('/error/400')
    else:
        return redirect('/error/500')

@api_view(['GET'])
def torneo_list_sencillo(request):
    try:
        torneos = Torneo.objects.all()
        serializer = TorneoSerializer(torneos, many=True)
        return Response(serializer.data)
    except Exception as e:
        return handle_error(request, f"Error al obtener la lista de torneos: {e}", status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def torneo_list(request):
    try:
        torneos = Torneo.objects.prefetch_related(
            'torneoparticipante_set__participante__usuario',
            'torneojugador_set__jugador__usuario'
        ).all()
        serializer = TorneoSerializerMejorado(torneos, many=True)
        return Response(serializer.data)
    except Exception as e:
        return handle_error(request, f"Error al obtener la lista de torneos: {e}", status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def equipo_list_sencillo(request):
    try:
        equipos = Equipo.objects.all()
        serializer = EquipoSerializerMejorado(equipos, many=True)
        return Response(serializer.data)
    except Exception as e:
        return handle_error(request, f"Error al obtener la lista de equipos: {e}", status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def participante_list_mejorado(request):
    try:
        participantes = Participante.objects.prefetch_related('participanteequipo_set').all()
        serializer = ParticipanteSerializerMejorado(participantes, many=True)
        return Response(serializer.data)
    except Exception as e:
        return handle_error(request, f"Error al obtener la lista de participantes: {e}", status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def juego_list_mejorado(request):
    try:
        juegos = Juego.objects.prefetch_related('torneos').all()
        serializer = JuegoSerializerMejorado(juegos, many=True)
        return Response(serializer.data)
    except Exception as e:
        return handle_error(request, f"Error al obtener la lista de juegos: {e}", status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def torneo_buscar(request):
    try:
        formulario = BusquedaTorneoForm(request.query_params)
        if formulario.is_valid():
            texto = formulario.data.get('textoBusqueda')
            torneos = Torneo.objects.prefetch_related("participantes", "juegos_torneo")
            torneos = torneos.filter(Q(nombre__contains=texto) | Q(descripcion__contains=texto)).all()
            serializer = TorneoSerializerMejorado(torneos, many=True)
            return Response(serializer.data)
        else:
            return Response(formulario.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return handle_error(request, f"Error al buscar torneos: {e}", status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def torneo_buscar_avanzado(request):
    try:
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
    except Exception as e:
        return handle_error(request, f"Error al buscar torneos avanzados: {e}", status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def equipo_buscar_avanzado(request):
    try:
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
    except Exception as e:
        return handle_error(request, f"Error al buscar equipos avanzados: {e}", status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def participante_buscar_avanzado(request):
    try:
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
    except Exception as e:
        return handle_error(request, f"Error al buscar participantes avanzados: {e}", status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def juego_buscar_avanzado(request):
    try:
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
    except Exception as e:
        return handle_error(request, f"Error al buscar juegos avanzados: {e}", status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def participante_list(request):
    try:
        participantes = Participante.objects.all()
        serializer = ParticipanteSerializer(participantes, many=True)
        return Response(serializer.data)
    except Exception as e:
        return handle_error(request, f"Error al obtener la lista de participantes: {e}", status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def categoria_list(request):
    try:
        categorias = Torneo.objects.values_list('categoria', flat=True).distinct()
        return Response(list(categorias))
    except Exception as e:
        return handle_error(request, f"Error al obtener la lista de categorías: {e}", status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def torneo_create(request):
    try:
        torneoCreateSerializer = TorneoSerializerCreate(data=request.data)
        if torneoCreateSerializer.is_valid():
            try:
                torneoCreateSerializer.save()
                return Response("Torneo CREADO")
            except serializers.ValidationError as error:
                return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(torneoCreateSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return handle_error(request, f"Error al crear el torneo: {e}", status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def torneo_obtener(request, torneo_id):
    try:
        torneo = Torneo.objects.prefetch_related("participantes").get(id=torneo_id)
        serializer = TorneoSerializerMejorado(torneo)
        return Response(serializer.data)
    except Torneo.DoesNotExist:
        return handle_error(request, "Torneo no encontrado", status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return handle_error(request, f"Error al obtener el torneo: {e}", status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PUT'])
def torneo_editar(request, torneo_id):
    try:
        torneo = Torneo.objects.get(id=torneo_id)
        torneoCreateSerializer = TorneoSerializerCreate(data=request.data, instance=torneo)
        if torneoCreateSerializer.is_valid():
            try:
                torneoCreateSerializer.save()
                return Response("Torneo EDITADO")
            except serializers.ValidationError as error:
                return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(torneoCreateSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Torneo.DoesNotExist:
        return handle_error(request, "Torneo no encontrado", status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return handle_error(request, f"Error al editar el torneo: {e}", status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PATCH'])
def torneo_actualizar_nombre(request, torneo_id):
    try:
        torneo = Torneo.objects.get(id=torneo_id)
        serializer = TorneoSerializerActualizarNombre(data=request.data, instance=torneo)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response("Torneo EDITADO")
            except Exception as error:
                return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Torneo.DoesNotExist:
        return handle_error(request, "Torneo no encontrado", status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return handle_error(request, f"Error al actualizar el nombre del torneo: {e}", status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
def torneo_eliminar(request, torneo_id):
    try:
        torneo = Torneo.objects.get(id=torneo_id)
        torneo.delete()
        return Response("Torneo ELIMINADO")
    except Torneo.DoesNotExist:
        return handle_error(request, "Torneo no encontrado", status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return handle_error(request, f"Error al eliminar el torneo: {e}", status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def consola_list(request):
    try:
        consolas = Consola.objects.all()
        serializer = ConsolaSerializer(consolas, many=True)
        return Response(serializer.data)
    except Exception as e:
        return handle_error(request, f"Error al obtener la lista de consolas: {e}", status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def juego_create(request):
    try:
        juegoCreateSerializer = JuegoSerializerCreate(data=request.data)
        if juegoCreateSerializer.is_valid():
            try:
                juegoCreateSerializer.save()
                return Response("Juego CREADO")
            except serializers.ValidationError as error:
                return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(juegoCreateSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return handle_error(request, f"Error al crear el juego: {e}", status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def juego_obtener(request, juego_id):
    try:
        juego = Juego.objects.select_related("torneo", "id_consola").get(id=juego_id)
        serializer = JuegoSerializerMejorado(juego)
        return Response(serializer.data)
    except Juego.DoesNotExist:
        return handle_error(request, "Juego no encontrado", status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return handle_error(request, f"Error al obtener el juego: {e}", status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PUT'])
def juego_editar(request, juego_id):
    try:
        juego = Juego.objects.get(id=juego_id)
        juegoCreateSerializer = JuegoSerializerCreate(data=request.data, instance=juego)
        if juegoCreateSerializer.is_valid():
            try:
                juegoCreateSerializer.save()
                return Response("Juego EDITADO")
            except serializers.ValidationError as error:
                return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(juegoCreateSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Juego.DoesNotExist:
        return handle_error(request, "Juego no encontrado", status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return handle_error(request, f"Error al editar el juego: {e}", status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PATCH'])
def juego_actualizar_nombre(request, juego_id):
    try:
        juego = Juego.objects.get(id=juego_id)
        serializer = JuegoSerializerActualizarNombre(data=request.data, instance=juego)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response("Juego EDITADO")
            except Exception as error:
                return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Juego.DoesNotExist:
        return handle_error(request, "Juego no encontrado", status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return handle_error(request, f"Error al actualizar el nombre del juego: {e}", status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
def juego_eliminar(request, juego_id):
    try:
        juego = Juego.objects.get(id=juego_id)
        juego.delete()
        return Response("Juego ELIMINADO")
    except Juego.DoesNotExist:
        return handle_error(request, "Juego no encontrado", status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return handle_error(request, f"Error al eliminar el juego: {e}", status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def usuario_list(request):
    try:
        usuarios = Usuario.objects.all()
        serializer = UsuarioSerializer(usuarios, many=True)
        return Response(serializer.data)
    except Exception as e:
        return handle_error(request, f"Error al obtener la lista de usuarios: {e}", status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def equipo_list(request):
    try:
        equipos = Equipo.objects.all()
        serializer = EquipoSerializer(equipos, many=True)
        return Response(serializer.data)
    except Exception as e:
        return handle_error(request, f"Error al obtener la lista de equipos: {e}", status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def participante_create(request):
    try:
        participanteCreateSerializer = ParticipanteSerializerCreate(data=request.data)
        if participanteCreateSerializer.is_valid():
            try:
                participanteCreateSerializer.save()
                return Response("Participante CREADO")
            except serializers.ValidationError as error:
                return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(participanteCreateSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return handle_error(request, f"Error al crear el participante: {e}", status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def participante_obtener(request, participante_id):
    try:
        participante = Participante.objects.prefetch_related("equipos").get(id=participante_id)
        serializer = ParticipanteSerializerMejorado(participante)
        return Response(serializer.data)
    except Participante.DoesNotExist:
        return handle_error(request, "Participante no encontrado", status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return handle_error(request, f"Error al obtener el participante: {e}", status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PUT'])
def participante_editar(request, participante_id):
    try:
        participante = Participante.objects.get(id=participante_id)
        participanteSerializer = ParticipanteSerializerCreate(data=request.data, instance=participante)
        if participanteSerializer.is_valid():
            try:
                participanteSerializer.save()
                return Response("Participante EDITADO")
            except serializers.ValidationError as error:
                return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(participanteSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Participante.DoesNotExist:
        return handle_error(request, "Participante no encontrado", status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return handle_error(request, f"Error al editar el participante: {e}", status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PATCH'])
def participante_actualizar_equipos(request, participante_id):
    try:
        participante = Participante.objects.get(id=participante_id)
        serializer = ParticipanteSerializerActualizarEquipos(data=request.data, instance=participante)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response("Equipos del participante ACTUALIZADOS")
            except Exception as error:
                return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Participante.DoesNotExist:
        return handle_error(request, "Participante no encontrado", status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return handle_error(request, f"Error al actualizar los equipos del participante: {e}", status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
def participante_eliminar(request, participante_id):
    try:
        participante = Participante.objects.get(id=participante_id)
        participante.delete()
        return Response("Participante ELIMINADO")
    except Participante.DoesNotExist:
        return handle_error(request, "Participante no encontrado", status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return handle_error(request, f"Error al eliminar el participante: {e}", status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def usuariologin_list(request):
    try:
        usuarios = UsuarioLogin.objects.all()
        serializer = UsuarioLoginSerializer(usuarios, many=True)
        return Response(serializer.data)
    except Exception as e:
        return handle_error(request, f"Error al obtener la lista de usuarios: {e}", status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def jugador_create(request):
    try:
        jugadorCreateSerializer = JugadorSerializerCreate(data=request.data)
        if jugadorCreateSerializer.is_valid():
            try:
                jugadorCreateSerializer.save()
                return Response("Jugador CREADO")
            except serializers.ValidationError as error:
                return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(jugadorCreateSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return handle_error(request, f"Error al crear el jugador: {e}", status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def jugador_obtener(request, jugador_id):
    try:
        jugador = Jugador.objects.prefetch_related("torneos").get(id=jugador_id)
        serializer = JugadorSerializer(jugador)
        return Response(serializer.data)
    except Jugador.DoesNotExist:
        return handle_error(request, "Jugador no encontrado", status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return handle_error(request, f"Error al obtener el jugador: {e}", status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PUT'])
def jugador_editar(request, jugador_id):
    try:
        jugador = Jugador.objects.get(id=jugador_id)
        jugadorSerializer = JugadorSerializerCreate(data=request.data, instance=jugador)
        if jugadorSerializer.is_valid():
            try:
                jugadorSerializer.save()
                return Response("Jugador EDITADO")
            except serializers.ValidationError as error:
                return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(jugadorSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Jugador.DoesNotExist:
        return handle_error(request, "Jugador no encontrado", status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return handle_error(request, f"Error al editar el jugador: {e}", status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PATCH'])
def jugador_actualizar_puntos(request, jugador_id):
    try:
        jugador = Jugador.objects.get(id=jugador_id)
        serializer = JugadorActualizarPuntosSerializer(data=request.data, instance=jugador)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response("Puntos del jugador ACTUALIZADOS")
            except Exception as error:
                return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Jugador.DoesNotExist:
        return handle_error(request, "Jugador no encontrado", status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return handle_error(request, f"Error al actualizar los puntos del jugador: {e}", status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
def jugador_eliminar_torneo(request, jugador_id, torneo_id):
    try:
        TorneoJugador.objects.get(jugador_id=jugador_id, torneo_id=torneo_id).delete()
        return Response("Jugador eliminado de este torneo")
    except TorneoJugador.DoesNotExist:
        return handle_error(request, "Jugador no encontrado en este torneo", status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return handle_error(request, f"Error al eliminar el jugador del torneo: {e}", status.HTTP_500_INTERNAL_SERVER_ERROR)

