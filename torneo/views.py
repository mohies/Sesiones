from django.shortcuts import render,redirect
from .models import *
from django.db.models import Prefetch,Count,Q
from .forms import *
from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import render, redirect
from .forms import RegistroForm
from .models import UsuarioLogin, Organizador, Jugador
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import authenticate, login,logout
from datetime import datetime


def index(request):
    if(not "fecha_inicio" in request.session):
        request.session["fecha_inicio"] = datetime.now().strftime('%d/%m/%Y %H:%M')
    return render(request, 'index.html')

def borrar_session(request):
    del request.session['fecha_inicio']
    return render(request, 'index.html')


def lista_torneo(request):
    # Prefetch para optimizar la carga de los jugadores
    torneos = Torneo.objects.prefetch_related('jugadores').all()

    # Si el usuario es un jugador, solo mostramos los torneos en los que está inscrito
    if request.user.groups.filter(name='Jugadores').exists():
        try:
            # Asegúrate de obtener el objeto 'Jugador' desde el usuario
            jugador = Jugador.objects.get(usuario=request.user)
            # Filtra los torneos en los que el jugador está inscrito
            torneos = torneos.filter(jugadores=jugador)
        except Jugador.DoesNotExist:
            # Si no existe un perfil de jugador para el usuario (por alguna razón)
            torneos = Torneo.objects.none()  # No muestra torneos si el jugador no tiene perfil

    context = {
        'torneos': torneos,
    }

    return render(request, 'torneo/lista_torneos.html', context)


def crear_torneo(request):
    
    datosFormulario = None
    if request.method == "POST":
        datosFormulario = request.POST
        
    formulario = TorneoForm(datosFormulario)
    if (request.method == "POST"):
        if formulario.is_valid():
            try:
                # Guarda el libro en la base de datos
                formulario.save()
                return redirect("lista_torneo")
            except Exception as error:
                print(error)
    
    return render(request, 'torneo/creartorneo/crear_torneo.html', {'formulario': formulario}) 



    
    
def torneo_buscar_avanzado(request):
    if len(request.GET) > 0:
        formulario = BusquedaAvanzadaTorneoForm(request.GET)
        if formulario.is_valid():
            mensaje_busqueda = "Se ha buscado por los siguientes valores:\n"
            QStorneos = Torneo.objects.prefetch_related("participantes")

            # Obtenemos los filtros del formulario
            textoBusqueda = formulario.cleaned_data.get('textoBusqueda')
            fechaDesde = formulario.cleaned_data.get('fecha_desde')
            fechaHasta = formulario.cleaned_data.get('fecha_hasta')

            # Si el usuario es un jugador, filtramos los torneos en los que está inscrito
            if request.user.groups.filter(name='Jugadores').exists():
                jugador = Jugador.objects.get(usuario=request.user)  # Obtén el jugador desde el usuario logueado
                
                # Filtra los torneos donde el jugador está inscrito como tal
                QStorneos = QStorneos.filter(jugadores=jugador)  # Filtra por los torneos del jugador

            # Por cada filtro comprobamos si tiene un valor y lo añadimos a la QuerySet
            if textoBusqueda != "":
                QStorneos = QStorneos.filter(Q(nombre__icontains=textoBusqueda) | Q(descripcion__icontains=textoBusqueda) | Q(categoria__contains=textoBusqueda))
                mensaje_busqueda += f" Nombre o contenido que contengan la palabra '{textoBusqueda}'\n"

            # Comprobamos las fechas
            if fechaDesde:
                mensaje_busqueda += f" Fecha desde: {fechaDesde.strftime('%d-%m-%Y')}\n"
                QStorneos = QStorneos.filter(fecha_inicio__gte=fechaDesde)

            if fechaHasta:
                mensaje_busqueda += f" Fecha hasta: {fechaHasta.strftime('%d-%m-%Y')}\n"
                QStorneos = QStorneos.filter(fecha_inicio__lte=fechaHasta)

            # Ejecutamos la consulta
            torneos = QStorneos.all()

            return render(request, 'torneo/creartorneo/buscar_torneo.html', {
                "torneos_mostrar": torneos,
                "texto_busqueda": mensaje_busqueda
            })
    else:
        formulario = BusquedaAvanzadaTorneoForm(None)

    return render(request, 'torneo/creartorneo/busqueda_avanzada.html', {"formulario": formulario})


@login_required
def torneo_jugador(request):
    if request.method == 'POST':
        formulario = TorneoJugadorForm(request.POST)
        if formulario.is_valid():
            torneo_seleccionado = formulario.cleaned_data['torneo']
            jugador = Jugador.objects.get(usuario=request.user)  # Obtén el jugador desde el usuario logueado

            # Verifica si el jugador ya está inscrito en el torneo
            if jugador not in torneo_seleccionado.jugadores.all():
                torneo_seleccionado.jugadores.add(jugador)  # Añade al jugador al torneo
                messages.success(request, f"Te has inscrito en el torneo: {torneo_seleccionado.nombre}")
            else:
                messages.warning(request, "Ya estás inscrito en este torneo.")

           
    else:
        formulario = TorneoJugadorForm()

    return render(request, 'torneo/torneo_jugador.html', {'formulario': formulario})



def registrar_usuario(request):
    if request.method == 'POST':
        # Formularios básicos y adicionales
        formulario = RegistroForm(request.POST)
        jugador_form = RegistroJugadorForm(request.POST) if 'rol' in request.POST and request.POST['rol'] == '2' else None
        organizador_form = RegistroOrganizadorForm(request.POST) if 'rol' in request.POST and request.POST['rol'] == '3' else None

        if formulario.is_valid():
            # Guardar el usuario
            user = formulario.save()

            # Obtener el rol seleccionado
            rol = int(formulario.cleaned_data.get('rol'))

            # Asignar el rol a través del campo 'rol' y agregarlo al grupo correspondiente
            if rol == UsuarioLogin.JUGADOR:
                # Guardamos los datos adicionales del Jugador
                if jugador_form and jugador_form.is_valid():
                    jugador = jugador_form.save(commit=False)
                    jugador.usuario = user
                    jugador.save()
                    # Añadir el usuario al grupo 'Jugadores'
                    grupo = Group.objects.get(name='Jugadores')
                    grupo.user_set.add(user)
                
            elif rol == UsuarioLogin.ORGANIZADOR:
                # Guardamos los datos adicionales del Organizador
                if organizador_form and organizador_form.is_valid():
                    organizador = organizador_form.save(commit=False)
                    organizador.usuario = user
                    organizador.save()
                    # Añadir el usuario al grupo 'Organizadores'
                    grupo = Group.objects.get(name='Organizadores')
                    grupo.user_set.add(user)

            # Si el rol no es Administrador, el login se realiza después del registro
            login(request, user)
            return redirect('index')  # Redirigir a la página principal o cualquier otra vista que desees

    else:
        # Crear instancias vacías de los formularios
        formulario = RegistroForm()
        jugador_form = RegistroJugadorForm()
        organizador_form = RegistroOrganizadorForm()

    # Renderizamos el formulario de registro, pasando los formularios contextuales
    return render(request, 'torneo/registration/signup.html', {
        'formulario': formulario,
        'jugador_form': jugador_form,
        'organizador_form': organizador_form
    })

@permission_required('torneo.add_torneo')
@login_required
def torneo_crear(request):
    if request.method == 'POST':
        formulario = TorneoForm(request.POST)
        if formulario.is_valid():
            try:
                formulario.save()
                # Redirigir a la lista de torneos sin pasar usuario_id
                return redirect("lista_torneo")
            except Exception as error:
                print(error)
                messages.error(request, "Hubo un error al crear el torneo.")
    else:
        formulario = TorneoForm(initial={"organizador": request.user})
    return render(request, 'torneo/create/crear.html', {'formulario': formulario})


@permission_required('torneo.change_torneo')
@login_required
def torneo_editarr(request, torneo_id):
    try:
        torneo = Torneo.objects.get(id=torneo_id)
    except Torneo.DoesNotExist:
        messages.error(request, "El torneo no existe.")
        return redirect("lista_torneo")

    if request.method == 'POST':
        formulario = TorneoForm(request.POST, instance=torneo)
        if formulario.is_valid():
            try:
                formulario.save()
                messages.success(request, "Torneo actualizado correctamente.")
                return redirect("lista_torneo")  # Adjusted to match URL name
            except Exception as error:
                print(error)
                messages.error(request, "Hubo un error al actualizar el torneo.")
    else:
        formulario = TorneoForm(instance=torneo)

    return render(request, 'torneo/create/edit.html', {'formulario': formulario, 'torneo': torneo})


@permission_required('torneo.delete_torneo')
@login_required
def torneo_eliminar(request, torneo_id):
    torneo = Torneo.objects.get(id=torneo_id)
    try:
        torneo.delete()
        messages.success(request, "Se ha eliminado el torneo " + torneo.nombre + " correctamente")
    except Exception as error:
        print(error)
    return redirect('lista_torneo')




@permission_required('torneo.view_torneo')
@login_required
def torneo_ver(request, torneo_id):
    try:
        torneo = Torneo.objects.get(id=torneo_id)
    except Torneo.DoesNotExist:
        messages.error(request, "El torneo no existe.")
        return redirect("lista_torneo")
    
    # Obtener los participantes y los jugadores del torneo
    participantes = torneo.participantes.all()
    jugadores = torneo.jugadores.all()

    # Pasar los datos a la plantilla
    return render(request, 'torneo/create/ver.html', {
        'torneo': torneo,
        'participantes': participantes,
        'jugadores': jugadores,
    })


#Distintos errores de las paginas web
def mi_error_404(request, exception=None):
    return render(request, 'torneo/errores/404.html', None,None,404)
def mi_error_400(request, exception=None):
    return render(request, 'torneo/errores/400.html', None,None,400)
def mi_error_403(request, exception=None):
    return render(request, 'torneo/errores/403.html', None,None,403)
def mi_error_500(request, exception=None):
    return render(request, 'torneo/errores/403.html', None,None,500)

