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
    # Verificar si la fecha de inicio está en la sesión, si no, agregarla
    if "fecha_inicio" not in request.session:
        request.session["fecha_inicio"] = datetime.now().strftime('%d/%m/%Y %H:%M')

    # Verificar si el nombre de usuario está en la sesión, si no, agregarlo
    if "nombre_usuario" not in request.session:
        request.session["nombre_usuario"] = request.user.username if request.user.is_authenticated else "Invitado"

    # Verificar si el estado del usuario está en la sesión, si no, agregarlo
    if "estado_usuario" not in request.session:
        request.session["estado_usuario"] = 'activo'  # Asignamos un valor por defecto como 'activo'

    # Verificar si las preferencias del usuario están en la sesión, si no, agregarlo
    if "preferencias_usuario" not in request.session:
        request.session["preferencias_usuario"] = {"idioma": "es", "notificaciones": True}  # Ejemplo de preferencias

    # Verificar si la última conexión está en la sesión, si no, agregarla
    if "ultima_conexion" not in request.session:
        request.session["ultima_conexion"] = datetime.now().strftime('%d/%m/%Y %H:%M')

    # Pasar los datos al template
    return render(request, 'index.html', {
        "fecha_inicio": request.session.get("fecha_inicio"),
        "nombre_usuario": request.user.username,  # Añadir el nombre del usuario autenticado
        "estado_usuario": request.session.get("estado_usuario"),
        "preferencias_usuario": request.session.get("preferencias_usuario"),
        "ultima_conexion": request.session.get("ultima_conexion"),
    })

def borrar_session(request):
    # Borrar todas las variables de la sesión
    session_keys = ['fecha_inicio', 'nombre_usuario', 'estado_usuario', 'preferencias_usuario', 'ultima_conexion']
    for key in session_keys:
        if key in request.session:
            del request.session[key]

    return render(request, 'index.html')  # Redirigir o renderizar la misma vista


def lista_torneo(request):
    torneos = Torneo.objects.prefetch_related('participantes__usuario').all()
    
    puede_editar = request.user.has_perm('torneo.change_torneo') if request.user.is_authenticated else False
    puede_eliminar = request.user.has_perm('torneo.delete_torneo') if request.user.is_authenticated else False

    context = {
        'torneos': torneos,
        'puede_editar': puede_editar,
        'puede_eliminar': puede_eliminar,
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
                return redirect("index")
            except Exception as error:
                print(error)
    
    return render(request, 'torneo/creartorneo/crear_torneo.html', {'formulario': formulario}) 


"""
def buscar_torneo(request):
    formulario = BusquedaTorneoForm(request.GET)

    if formulario.is_valid():
        texto = formulario.cleaned_data.get('textoBusqueda')
        torneos = Torneo.objects.all()
        torneos = torneos.filter(
            Q(nombre__icontains=texto) | Q(descripcion__icontains=texto)
        ).all()

        mensaje_busqueda = f"Se buscaron torneos que contienen en su nombre o contenido la palabra: {texto}"

        return render(request, 'torneo/formulario/buscar_torneo.html', {
            "torneos_mostrar": torneos,
            "texto_busqueda": mensaje_busqueda
        })
    
    # Si no se envió una búsqueda o la validación no fue correcta, redirigimos
    if "HTTP_REFERER" in request.META:
        return redirect(request.META["HTTP_REFERER"])
    else:
        return redirect('index')"""
    
    
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
            duracionMinima = formulario.cleaned_data.get('duracion_minima')
            
            
            # Por cada filtro comprobamos si tiene un valor y lo añadimos a la QuerySet
            if textoBusqueda != "":
                QStorneos = QStorneos.filter(Q(nombre__icontains=textoBusqueda) | Q(descripcion__icontains=textoBusqueda) |Q(categoria__contains=textoBusqueda))
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


def registrar_usuario(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        jugador_form = RegistroJugadorForm(request.POST) if 'rol' in request.POST and request.POST['rol'] == '2' else None
        organizador_form = RegistroOrganizadorForm(request.POST) if 'rol' in request.POST and request.POST['rol'] == '3' else None

        if form.is_valid():
            # Guardamos el usuario
            user = form.save()

            # Si es Jugador, también guardamos la información adicional de Jugador
            if jugador_form and jugador_form.is_valid():
                jugador = jugador_form.save(commit=False)
                jugador.usuario = user
                jugador.save()

            # Si es Organizador, también guardamos la información adicional de Organizador
            if organizador_form and organizador_form.is_valid():
                organizador = organizador_form.save(commit=False)
                organizador.usuario = user
                organizador.save()

            login(request, user)  # Iniciar sesión después del registro
            return redirect('index')  # Redirigir a la página principal o alguna otra

    else:
        form = RegistroForm()
        jugador_form = RegistroJugadorForm()
        organizador_form = RegistroOrganizadorForm()

    return render(request, 'torneo/registration/signup.html', {
        'formulario': form,
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
                return redirect("torneo_lista_usuario", usuario_id=request.user.id)
            except Exception as error:
                print(error)
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
        return redirect("torneo_lista_usuario", usuario_id=request.user.id)

    if request.method == 'POST':
        formulario = TorneoForm(request.POST, instance=torneo)
        if formulario.is_valid():
            try:
                formulario.save()
                messages.success(request, "Torneo actualizado correctamente.")
                return redirect("torneo_lista_usuario", usuario_id=request.user.id)
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

    return render(request, 'torneo/create/ver.html', {'torneo': torneo})











#Distintos errores de las paginas web
def mi_error_404(request, exception=None):
    return render(request, 'torneo/errores/404.html', None,None,404)
def mi_error_400(request, exception=None):
    return render(request, 'torneo/errores/400.html', None,None,400)
def mi_error_403(request, exception=None):
    return render(request, 'torneo/errores/403.html', None,None,403)
def mi_error_500(request, exception=None):
    return render(request, 'torneo/errores/403.html', None,None,500)

