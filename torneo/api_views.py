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
from django.contrib.auth.decorators import permission_required
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


"""
    Realizar las operaciones de POST, PUT, PATCH y DELETE de un modelo, con sus validaciones(al menos 3 campos), control de errores y respuestas.
    (1 punto ,0,25:POST, 0,25: PUT, 0,25:PATCH, 0,25-DELETE)
    
    Incluir en la aplicación algún modelo(Puede repetirse con alguno de los anteriores) un campo que sea un archivo, y 
    gestionar las peticiones GET, POST, PUT, PATCH y DELETE de ese campo(1 punto)
"""
@api_view(['GET'])
def categoria_list(request):
    try:
        categorias = Torneo.objects.values_list('categoria', flat=True).distinct()
        return Response(list(categorias))
    except Exception as e:
        return handle_error(request, f"Error al obtener la lista de categorías: {e}", status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_required('torneo.add_torneo', raise_exception=True)
def torneo_create(request):
    """
    🔹 Crea un torneo asignando automáticamente el usuario autenticado como organizador.
    """
    try:
        print(f"Usuario autenticado: {request.user}")  # Ver quién está autenticado

        datos = request.data.copy()
        datos["organizador"] = request.user.id  #  Asignar automáticamente el organizador

        serializer = TorneoSerializerCreate(data=datos, context={"request": request})
        if serializer.is_valid():
            torneo = serializer.save()
            print(f"Torneo creado: {torneo.nombre} | Organizador: {torneo.organizador}")  #  Debug
            return Response({"mensaje": "Torneo creado exitosamente", "id": torneo.id}, status=status.HTTP_201_CREATED)
        else:
            print(f"Errores en el serializer: {serializer.errors}")  # Debug
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        print(f"Error al crear torneo: {e}")  # 📌 Debug
        return Response({"error": f"Error al crear el torneo: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



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
@permission_required('torneo.change_torneo', raise_exception=True)
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
@permission_required('torneo.change_torneo', raise_exception=True)
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
    
@api_view(['PATCH'])
@permission_required('torneo.change_torneo', raise_exception=True)
def torneo_actualizar_imagen(request, torneo_id):
    try:
        # Verificar si el torneo existe
        torneo = Torneo.objects.get(id=torneo_id)

        # Verificar si se ha enviado una imagen en la solicitud
        if 'imagen' in request.FILES:
            imagen = request.FILES['imagen']
            torneo.imagen = imagen
            torneo.save()
            return Response({"mensaje": "Imagen actualizada correctamente"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "No se ha seleccionado ninguna imagen."}, status=status.HTTP_400_BAD_REQUEST)

    except Torneo.DoesNotExist:
        return Response({"error": "Torneo no encontrado"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": f"Error al actualizar la imagen: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
@permission_required('torneo.delete_torneo', raise_exception=True)
def torneo_eliminar_imagen(request, torneo_id):
    """
    Elimina la imagen de un torneo específico.
    """
    try:
        # Verificar si el torneo existe
        torneo = Torneo.objects.get(id=torneo_id)

        # Verificar si tiene una imagen y eliminarla
        if torneo.imagen:
            torneo.imagen.delete()  # Esto elimina el archivo físico
            torneo.imagen = None
            torneo.save()
            return Response({"mensaje": "Imagen eliminada correctamente"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "El torneo no tiene una imagen asignada"}, status=status.HTTP_400_BAD_REQUEST)
    
    except Torneo.DoesNotExist:
        return Response({"error": "Torneo no encontrado"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": f"Error al eliminar la imagen: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





@api_view(['DELETE'])
@permission_required('torneo.delete_torneo', raise_exception=True)
def torneo_eliminar(request, torneo_id):
    try:
        torneo = Torneo.objects.get(id=torneo_id)
        torneo.delete()
        return Response("Torneo ELIMINADO")
    except Torneo.DoesNotExist:
        return handle_error(request, "Torneo no encontrado", status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return handle_error(request, f"Error al eliminar el torneo: {e}", status.HTTP_500_INTERNAL_SERVER_ERROR)



"""
    Realizar las operaciones de POST, PUT, PATCH y DELETE de un modelo con relaciones ManyToOne con sus validaciones(al menos 3 campos), 
    control de errores y respuestas.(1 punto ,0,25:POST, 0,25: PUT, 0,25:PATCH, 0,25-DELETE)
"""

@api_view(['GET'])
def consola_list(request):
    try:
        consolas = Consola.objects.all()
        serializer = ConsolaSerializer(consolas, many=True)
        return Response(serializer.data)
    except Exception as e:
        return handle_error(request, f"Error al obtener la lista de consolas: {e}", status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_required('torneo.add_juego', raise_exception=True)  
def juego_create(request):
    """
    🔹 Crea un juego asignando automáticamente el usuario autenticado como creador.
    """
    try:
        if not request.user or not request.user.is_authenticated:  # Verificamos autenticación
            return Response({"error": "Usuario no autenticado"}, status=status.HTTP_401_UNAUTHORIZED)

        print(f"Usuario autenticado: {request.user}") 

        # Copiamos los datos y asignamos el usuario autenticado como creador
        datos = request.data.copy()
        serializer = JuegoSerializerCreate(data=datos)

        if serializer.is_valid():
            juego = serializer.save()  
            
            if hasattr(juego, "creador"):  #  Verificar que el campo "creador" existe en el modelo
                juego.creador = request.user  
                juego.save()
                print(f"Juego creado: {juego.nombre} | Creador: {juego.creador.username}") 
            else:
                print(" Error: El modelo Juego no tiene un campo 'creador'.")

            return Response({"mensaje": "Juego creado exitosamente", "id": juego.id}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        print(f"Error al crear juego: {e}") 
        return Response({"error": f"Error al crear el juego: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



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
@permission_required('torneo.change_juego', raise_exception=True)
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
@permission_required('torneo.change_juego', raise_exception=True)
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
@permission_required('torneo.delete_juego', raise_exception=True)
def juego_eliminar(request, juego_id):
    try:
        juego = Juego.objects.get(id=juego_id)
        juego.delete()
        return Response("Juego ELIMINADO")
    except Juego.DoesNotExist:
        return handle_error(request, "Juego no encontrado", status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return handle_error(request, f"Error al eliminar el juego: {e}", status.HTTP_500_INTERNAL_SERVER_ERROR)
    
"""
  Realizar las operaciones de POST, PUT, PATCH y DELETE de un modelo con una relacion ManyToMany distinto al anterior,con sus validaciones
  (al menos 3 campos), control de errores y respuestas.(1 punto ,0,25:POST, 0,25: PUT, 0,25:PATCH, 0,25-DELETE)
"""

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
@permission_required('torneo.add_participante', raise_exception=True)
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
@permission_required('torneo.change_participante', raise_exception=True)
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
@permission_required('torneo.change_participante', raise_exception=True)
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
@permission_required('torneo.delete_participante', raise_exception=True)
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



"""
Realizar las operaciones de POST, PUT, PATCH y DELETE de un modelo con relaciones ManyToMany con tabla intermedia distinto al anterior, 
con sus validaciones(al menos 3 campos), control de errores y respuestas.(1 punto ,0,25:POST, 0,25: PUT, 0,25:PATCH, 0,25-DELETE)
"""

@api_view(['POST'])
@permission_required('torneo.add_jugador')
def jugador_create(request):
    try:
        # Obtener el jugador autenticado
        jugador = Jugador.objects.filter(usuario=request.user).first()
        if not jugador:
            return Response({"error": "Usuario no autenticado o no tiene perfil de jugador"}, status=status.HTTP_404_NOT_FOUND)

        # Obtener torneos y validar
        torneos_ids = request.data.get("torneos", [])
        if not torneos_ids:
            return Response({"error": "Debe proporcionar al menos un torneo"}, status=status.HTTP_400_BAD_REQUEST)

        torneos_validos = Torneo.objects.filter(id__in=torneos_ids)
        if torneos_validos.count() != len(torneos_ids):
            return Response({"error": "Uno o más torneos no existen"}, status=status.HTTP_400_BAD_REQUEST)

        # Asociar jugador a torneos, evitando duplicados
        torneos_asociados = []
        for torneo in torneos_validos:
            if TorneoJugador.objects.filter(torneo=torneo, jugador=jugador).exists():
                return Response({"error": f"Ya estás inscrito en el torneo {torneo.nombre}"}, status=status.HTTP_400_BAD_REQUEST)
            TorneoJugador.objects.create(torneo=torneo, jugador=jugador)
            torneos_asociados.append(torneo.nombre)

        return Response({"mensaje": "Jugador asociado a los torneos correctamente", "torneos": torneos_asociados}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": f"Error al asociar el jugador al torneo: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
@permission_required('torneo.change_jugador', raise_exception=True)
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
@permission_required('torneo.change_jugador', raise_exception=True)
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
@permission_required('torneo.delete_jugador', raise_exception=True)
def jugador_eliminar_torneo(request, jugador_id, torneo_id):
    try:
        TorneoJugador.objects.get(jugador_id=jugador_id, torneo_id=torneo_id).delete()
        return Response("Jugador eliminado de este torneo")
    except TorneoJugador.DoesNotExist:
        return handle_error(request, "Jugador no encontrado en este torneo", status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return handle_error(request, f"Error al eliminar el jugador del torneo: {e}", status.HTTP_500_INTERNAL_SERVER_ERROR)

# api/views.py (en el servidor)

# views.py
from django.contrib.auth.models import Group
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import UsuarioLogin, Jugador, Organizador
from .serializers import UsuarioSerializerRegistro


class RegistrarUsuarioView(generics.CreateAPIView):
    serializer_class = UsuarioSerializerRegistro
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        # Creamos el serializer con los datos recibidos
        serializers = UsuarioSerializerRegistro(data=request.data)
        
        # Verificamos si los datos del formulario son válidos
        if serializers.is_valid():
            try:
                # Obtenemos el rol desde los datos enviados
                rol = request.data.get('rol')
                
                # Creamos el usuario con los datos del formulario
                user = UsuarioLogin.objects.create_user(
                    username=serializers.validated_data.get("username"),
                    email=serializers.validated_data.get("email"),
                    password=serializers.validated_data.get("password1"),  # Usamos password1
                    rol=rol  #Establecemos el rol aquí
                )

                # Asignamos el usuario al grupo correspondiente según su rol
                if rol == str(UsuarioLogin.JUGADOR):  # Comparamos como string porque cuando le hacemos un reques data .get viene como tipo string no entero
                    grupo = Group.objects.get(name='Jugadores')
                    grupo.user_set.add(user)
                    Jugador.objects.create(usuario=user)  # Crear una instancia de Jugador
                elif rol == str(UsuarioLogin.ORGANIZADOR):  # Comparamos como string
                    grupo = Group.objects.get(name='Organizadores')
                    grupo.user_set.add(user)
                    Organizador.objects.create(usuario=user)  # Crear una instancia de Organizador

                # Serializamos el usuario creado para la respuesta
                usuarioSerializado = UsuarioLoginSerializer(user)
                
                # Devolvemos la respuesta con el usuario serializado
                return Response(usuarioSerializado.data, status=status.HTTP_201_CREATED)

            except Exception as error:
                # Si ocurre un error, lo capturamos y devolvemos un error 500
                print(repr(error))
                return Response({"error": str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            # Si los datos del serializer no son válidos, devolvemos los errores
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
@api_view(['GET'])
def torneos_usuario(request):
    """
    Devuelve la lista de torneos en los que el usuario autenticado está inscrito.
    """
    # Buscar torneos en los que el usuario esté como jugador
    torneos = Torneo.objects.filter(torneojugador__jugador__usuario=request.user).distinct()
    
    # Serializar y devolver los datos
    serializer = TorneoSerializer(torneos, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def torneos_usuario_con_jugadores(request):
    """
     Devuelve la lista de torneos en los que el usuario autenticado está inscrito,
       junto con la lista de jugadores que participan en cada torneo.
    """
    # Buscar torneos en los que el usuario está inscrito como jugador
    torneos = Torneo.objects.filter(torneojugador__jugador__usuario=request.user).distinct()

    # Serializar los torneos con la lista de jugadores
    serializer = TorneoSerializer(torneos, many=True)

    # Agregar la lista de jugadores en cada torneo
    for torneo in serializer.data:
        jugadores = Jugador.objects.filter(torneojugador__torneo_id=torneo["id"]).select_related("usuario")
        torneo["jugadores"] = [
            {"id": jugador.id, "username": jugador.usuario.username, "puntos": jugador.puntos}
            for jugador in jugadores
        ]

    return Response(serializer.data, status=status.HTTP_200_OK)



from oauth2_provider.models import AccessToken
@api_view(['GET'])
def obtener_usuario_token(request, token):
    ModeloToken = AccessToken.objects.get(token=token)
    usuario = UsuarioLogin.objects.get(id=ModeloToken.user_id)
    serializer = UsuarioLoginSerializer(usuario)
    return Response(serializer.data)


