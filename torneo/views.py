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


def index(request):
    return render(request, 'index.html')

def lista_torneo(request):
    torneos = Torneo.objects.prefetch_related('participantes__usuario').all()
    return render(request, 'torneo/lista_torneos.html', {'torneos': torneos})



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


def torneo_editar(request, torneo_id):
    # Obtenemos el torneo correspondiente al ID proporcionado
    torneo = Torneo.objects.get(id=torneo_id)
    
    datosFormulario = None  # Inicializamos la variable para los datos del formulario

    if request.method == "POST":
        datosFormulario = request.POST  # Capturamos los datos enviados por el formulario
    
    # Creamos el formulario usando la instancia del torneo actual
    formulario = TorneoForm(datosFormulario, instance=torneo)
    
    if request.method == "POST":
        if formulario.is_valid():  # Validamos el formulario
            try:
                # Guardamos los cambios en la base de datos
                formulario.save()
                # Mostramos un mensaje de éxito
                messages.success(
                    request,
                    f"Se ha editado el torneo '{formulario.cleaned_data.get('nombre')}' correctamente."
                )
                return redirect('lista_torneo')  # Redirigimos a la lista de torneos
            except Exception as error:
                print(error)  # Imprimimos el error en la consola para depuración
    
    # Renderizamos el formulario de edición
    return render(
        request,
        'torneo/creartorneo/crear_torneo.html',
        {"formulario": formulario, "torneo": torneo}
    )
    
    
def torneo_eliminar(request, torneo_id):
    torneo = Torneo.objects.get(id=torneo_id)
    try:
        torneo.delete()
        messages.success(request, "Se ha eliminado el torneo " + torneo.nombre + " correctamente")
    except Exception as error:
        print(error)
    return redirect('lista_torneo')



def crear_equipo(request):
    datosFormulario = None  # Esto es para capturar los datos del formulario si se envían por POST

    # Si la solicitud es POST, significa que se está enviando el formulario
    if request.method == "POST":
        datosFormulario = request.POST
        
    formulario = EquipoForm(datosFormulario)  # Creamos una instancia del formulario con los datos de la solicitud
    if request.method == "POST" and formulario.is_valid():  # Si el formulario es válido
        try:
            formulario.save()  # Guarda el equipo en la base de datos
            return redirect("index")  # Redirige al índice o la página que queramos
        except Exception as error:
            print(error)  # Imprime el error si ocurre alguno

    return render(request, 'torneo/crearequipo/crear_equipo.html', {'formulario': formulario})  # Renderiza el formulario


def lista_equipos(request):
    # Recuperar todos los equipos desde la base de datos
    equipos = Equipo.objects.all()

    # Pasar la lista de equipos a la plantilla
    return render(request, 'torneo/lista_equipos.html', {
        'equipos': equipos
    })

def equipo_buscar_avanzado(request):
    if len(request.GET) > 0:
        formulario = BusquedaAvanzadaEquipoForm(request.GET)
        if formulario.is_valid():
            
            mensaje_busqueda = "Se ha buscado por los siguientes valores:\n"
            
            QSequipos = Equipo.objects
            
            # Obtenemos los filtros del formulario
            textoBusqueda = formulario.cleaned_data.get('textoBusqueda')
            fecha_ingreso_desde = formulario.cleaned_data.get('fecha_ingreso_desde')
            fecha_ingreso_hasta = formulario.cleaned_data.get('fecha_ingreso_hasta')
            puntos_minimos = formulario.cleaned_data.get('puntos_minimos')
            puntos_maximos = formulario.cleaned_data.get('puntos_maximos')
            
            # Aplicamos los filtros según corresponda
            if textoBusqueda:
                QSequipos = QSequipos.filter(Q(nombre__icontains=textoBusqueda))
                mensaje_busqueda += f" Nombre que contenga la palabra '{textoBusqueda}'\n"
            
            if fecha_ingreso_desde:
                QSequipos = QSequipos.filter(fecha_ingreso__gte=fecha_ingreso_desde)
                mensaje_busqueda += f" Fecha de ingreso desde: {fecha_ingreso_desde.strftime('%d-%m-%Y')}\n"
            
            if fecha_ingreso_hasta:
                QSequipos = QSequipos.filter(fecha_ingreso__lte=fecha_ingreso_hasta)
                mensaje_busqueda += f" Fecha de ingreso hasta: {fecha_ingreso_hasta.strftime('%d-%m-%Y')}\n"
            
            if puntos_minimos is not None:
                QSequipos = QSequipos.filter(puntos_contribuidos__gte=puntos_minimos)
                mensaje_busqueda += f" Puntos mínimos: {puntos_minimos}\n"
            
            if puntos_maximos is not None:
                QSequipos = QSequipos.filter(puntos_contribuidos__lte=puntos_maximos)
                mensaje_busqueda += f" Puntos máximos: {puntos_maximos}\n"
            
            # Ejecutamos la consulta
            equipos = QSequipos.all()
    
            return render(request, 'torneo/crearequipo/buscar_equipo.html', {
                "equipos_mostrar": equipos,
                "texto_busqueda": mensaje_busqueda
            })
    else:
        formulario = BusquedaAvanzadaEquipoForm(None)
    
    return render(request, 'torneo/crearequipo/busqueda_avanzada.html', {"formulario": formulario})



def equipo_editar(request, equipo_id):
    # Obtenemos el equipo correspondiente al ID proporcionado
    equipo = Equipo.objects.get(id=equipo_id)
    
    datosFormulario = None  # Inicializamos la variable para los datos del formulario

    if request.method == "POST":
        datosFormulario = request.POST  # Capturamos los datos enviados por el formulario
    
    # Creamos el formulario usando la instancia del equipo actual
    formulario = EquipoForm(datosFormulario, instance=equipo)
    
    if request.method == "POST":
        if formulario.is_valid():  # Validamos el formulario
            try:
                # Guardamos los cambios en la base de datos
                formulario.save()
                # Mostramos un mensaje de éxito
                messages.success(
                    request,
                    f"Se ha editado el equipo '{formulario.cleaned_data.get('nombre')}' correctamente."
                )
                return redirect('lista_equipos')  # Redirigimos a la lista de equipos
            except Exception as error:
                print(error)  # Imprimimos el error en la consola para depuración
    
    # Renderizamos el formulario de edición
    return render(
        request,
        'torneo/crearequipo/crear_equipo.html',  
        {"formulario": formulario, "equipo": equipo}
    )
    
    
def equipo_eliminar(request, equipo_id):
    equipo = Equipo.objects.get(id=equipo_id)
    try:
        equipo.delete()
        messages.success(request, "Se ha eliminado el equipo " + equipo.nombre + " correctamente")
    except Exception as error:
        print(error)
    return redirect('lista_equipos')


def crear_participante(request):
    datosFormulario = None
    if request.method == "POST":
        datosFormulario = request.POST
    
    formulario = ParticipanteForm(datosFormulario)
    
    if request.method == "POST":
        if formulario.is_valid():
            try:
                # Guarda el participante en la base de datos
                formulario.save()
                return redirect("index")  # Redirige a la página principal o cualquier otra vista
            except Exception as error:
                print(error)
    
    return render(request, 'torneo/crearparticipante/crear_participante.html', {'formulario': formulario})



def participante_buscar_avanzado(request):
    if len(request.GET) > 0:
        formulario = BusquedaAvanzadaParticipanteForm(request.GET)
        if formulario.is_valid():
            
            mensaje_busqueda = "Se ha buscado por los siguientes valores:\n"
            
            QSparticipantes = Participante.objects.select_related("usuario").prefetch_related("equipos")
            
            # Obtenemos los filtros del formulario
            textoBusqueda = formulario.cleaned_data.get('textoBusqueda')
            fecha_inscripcion_desde = formulario.cleaned_data.get('fecha_inscripcion_desde')
            fecha_inscripcion_hasta = formulario.cleaned_data.get('fecha_inscripcion_hasta')
            puntos_minimos = formulario.cleaned_data.get('puntos_minimos')
            puntos_maximos = formulario.cleaned_data.get('puntos_maximos')
            tiempo_jugado_minimo = formulario.cleaned_data.get('tiempo_jugado_minimo')
            tiempo_jugado_maximo = formulario.cleaned_data.get('tiempo_jugado_maximo')
            equipos = formulario.cleaned_data.get('equipos')
            
            # Aplicamos los filtros según corresponda
            if textoBusqueda:
                QSparticipantes = QSparticipantes.filter(Q(usuario__nombre__icontains=textoBusqueda))
                mensaje_busqueda += f" Nombre del participante que contenga la palabra '{textoBusqueda}'\n"
            
            if fecha_inscripcion_desde:
                QSparticipantes = QSparticipantes.filter(fecha_inscripcion__gte=fecha_inscripcion_desde)
                mensaje_busqueda += f" Fecha de inscripción desde: {fecha_inscripcion_desde.strftime('%d-%m-%Y')}\n"
            
            if fecha_inscripcion_hasta:
                QSparticipantes = QSparticipantes.filter(fecha_inscripcion__lte=fecha_inscripcion_hasta)
                mensaje_busqueda += f" Fecha de inscripción hasta: {fecha_inscripcion_hasta.strftime('%d-%m-%Y')}\n"
            
            if puntos_minimos is not None:
                QSparticipantes = QSparticipantes.filter(puntos_obtenidos__gte=puntos_minimos)
                mensaje_busqueda += f" Puntos obtenidos mínimos: {puntos_minimos}\n"
            
            if puntos_maximos is not None:
                QSparticipantes = QSparticipantes.filter(puntos_obtenidos__lte=puntos_maximos)
                mensaje_busqueda += f" Puntos obtenidos máximos: {puntos_maximos}\n"
            
            if tiempo_jugado_minimo is not None:
                QSparticipantes = QSparticipantes.filter(tiempo_jugado__gte=tiempo_jugado_minimo)
                mensaje_busqueda += f" Tiempo jugado mínimo: {tiempo_jugado_minimo} horas\n"
            
            if tiempo_jugado_maximo is not None:
                QSparticipantes = QSparticipantes.filter(tiempo_jugado__lte=tiempo_jugado_maximo)
                mensaje_busqueda += f" Tiempo jugado máximo: {tiempo_jugado_maximo} horas\n"
                
            if equipos is not None:
                # Extraer los nombres de los equipos (solo el campo 'nombre' de cada objeto Equipo)
                nombres_equipos = equipos.values_list('nombre', flat=True)

                # Filtrar QSparticipantes por los nombres de los equipos
                QSparticipantes = QSparticipantes.filter(equipos__nombre__in=nombres_equipos)

                # Actualizar el mensaje de búsqueda con los nombres de los equipos
                mensaje_busqueda += f" Buscado por equipos: {', '.join(nombres_equipos)} \n"

            # Ejecutamos la consulta
            participantes = QSparticipantes.all()
    
            return render(request, 'torneo/crearparticipante/buscar_participante.html', {
                "participantes_mostrar": participantes,
                "texto_busqueda": mensaje_busqueda
            })
    else:
        formulario = BusquedaAvanzadaParticipanteForm(None)
    
    return render(request, 'torneo/crearparticipante/busqueda_avanzada.html', {"formulario": formulario})



def lista_participantes(request):
    # Recuperar todos los participantes desde la base de datos
    participantes = Participante.objects.all()

    # Pasar la lista de participantes a la plantilla
    return render(request, 'torneo/lista_participantes.html', {
        'participantes': participantes
    })

def participante_editar(request, participante_id):
    # Obtenemos el participante correspondiente al ID proporcionado
    participante = Participante.objects.get(id=participante_id)
    
    datosFormulario = None  # Inicializamos la variable para los datos del formulario

    if request.method == "POST":
        datosFormulario = request.POST  # Capturamos los datos enviados por el formulario
    
    # Creamos el formulario usando la instancia del participante actual
    formulario = ParticipanteForm(datosFormulario, instance=participante)
    
    if request.method == "POST":
        if formulario.is_valid():  # Validamos el formulario
            try:
                # Guardamos los cambios en la base de datos
                formulario.save()
                # Mostramos un mensaje de éxito
                messages.success(
                    request,
                    f"Se ha editado el participante '{formulario.cleaned_data.get('usuario.nombre')}' correctamente."
                )
                return redirect('lista_participantes')  # Redirigimos a la lista de participantes
            except Exception as error:
                print(error)  # Imprimimos el error en la consola para depuración
    
    # Renderizamos el formulario de edición
    return render(
        request,
        'torneo/crearparticipante/crear_participante.html',  
        {"formulario": formulario, "participante": participante}
    )

def participante_eliminar(request, participante_id):
    participante = Participante.objects.get(id=participante_id)  # Obtenemos el participante al igual que el equipo
    try:
        participante.delete()  # Eliminamos el participante
        messages.success(request, "Se ha eliminado el participante " + participante.usuario.nombre + " correctamente")
    except Exception as error:
        print(error)  # Si ocurre un error, lo mostramos en la consola
    return redirect('lista_participantes')  # Redirigimos a la lista de participantes



def crear_usuario(request):
    datosFormulario = None  # Inicializamos la variable para los datos del formulario

    if request.method == "POST":
        datosFormulario = request.POST  # Capturamos los datos enviados por el formulario
    
    # Creamos el formulario
    formulario = UsuarioForm(datosFormulario)

    if request.method == "POST":
        if formulario.is_valid():  # Validamos el formulario
            try:
                # Guardamos el usuario en la base de datos
                formulario.save()
                # Mostramos un mensaje de éxito
                messages.success(request, "El usuario ha sido creado correctamente.")
                return redirect("lista_usuarios")  # Redirigimos a la lista de usuarios
            except Exception as error:
                print(error)  # Imprimimos el error en la consola para depuración

    return render(request, 'torneo/crearusuario/crear_usuario.html', {'formulario': formulario})


def usuario_buscar_avanzado(request):
    if len(request.GET) > 0:
        formulario = BusquedaUsuarioForm(request.GET)
        if formulario.is_valid():
            
            mensaje_busqueda = "Se ha buscado por los siguientes valores:\n"
            
            QSusarios = Usuario.objects
            
            # Obtenemos los filtros del formulario
            textoBusqueda = formulario.cleaned_data.get('textoBusqueda')
            fecha_registro_desde = formulario.cleaned_data.get('fecha_registro_desde')
            fecha_registro_hasta = formulario.cleaned_data.get('fecha_registro_hasta')
            
            # Aplicamos los filtros según corresponda
            if textoBusqueda:
                QSusarios = QSusarios.filter(Q(nombre__icontains=textoBusqueda) | Q(correo__icontains=textoBusqueda))
                mensaje_busqueda += f" Nombre o correo que contenga la palabra '{textoBusqueda}'\n"
            
            if fecha_registro_desde:
                QSusarios = QSusarios.filter(fecha_registro__gte=fecha_registro_desde)
                mensaje_busqueda += f" Fecha de registro desde: {fecha_registro_desde.strftime('%d-%m-%Y')}\n"
            
            if fecha_registro_hasta:
                QSusarios = QSusarios.filter(fecha_registro__lte=fecha_registro_hasta)
                mensaje_busqueda += f" Fecha de registro hasta: {fecha_registro_hasta.strftime('%d-%m-%Y')}\n"
            
            # Ejecutamos la consulta
            usuarios = QSusarios.all()

            if not usuarios.exists():
                messages.info(request, 'No se encontraron usuarios con los filtros aplicados.')

            return render(request, 'torneo/crearusuario/buscar_usuario.html', {
                "usuarios_mostrar": usuarios,
                "texto_busqueda": mensaje_busqueda
            })
    else:
        formulario = BusquedaUsuarioForm(None)
    
    return render(request, 'torneo/crearusuario/busqueda_avanzada.html', {"formulario": formulario})


def lista_usuarios(request):
    # Obtener todos los usuarios de la base de datos
    usuarios = Usuario.objects.all()
    
    # Pasar los usuarios a la plantilla
    return render(request, 'torneo/lista_usuarios.html', {
        'usuarios': usuarios
    })


def usuario_editar(request, usuario_id):
    # Obtenemos el usuario correspondiente al ID proporcionado
    usuario = Usuario.objects.get(id=usuario_id)
    
    datosFormulario = None  # Inicializamos la variable para los datos del formulario

    if request.method == "POST":
        datosFormulario = request.POST  # Capturamos los datos enviados por el formulario
    
    # Creamos el formulario usando la instancia del usuario actual
    formulario = UsuarioForm(datosFormulario, instance=usuario)
    
    if request.method == "POST":
        if formulario.is_valid():  # Validamos el formulario
            try:
                # Guardamos los cambios en la base de datos
                formulario.save()
                # Mostramos un mensaje de éxito
                messages.success(
                    request,
                    f"Se ha editado el usuario '{formulario.cleaned_data.get('nombre')}' correctamente."
                )
                return redirect('lista_usuarios')  # Redirigimos a la lista de usuarios
            except Exception as error:
                print(error)  # Imprimimos el error en la consola para depuración
    
    # Renderizamos el formulario de edición
    return render(
        request,
        'torneo/crearusuario/crear_usuario.html',  
        {"formulario": formulario, "usuario": usuario}
    )

def usuario_eliminar(request, usuario_id):
    try:
        # Obtenemos el usuario al igual que el participante
        usuario = Usuario.objects.get(id=usuario_id)
        
        # Eliminamos el usuario
        usuario.delete()
        
        # Mostramos un mensaje de éxito
        messages.success(request, f"Se ha eliminado el usuario {usuario.nombre} correctamente.")
        
    except Usuario.DoesNotExist:
        # Si el usuario no existe, mostramos un mensaje de error
        messages.error(request, "El usuario no existe.")
    except Exception as error:
        # Si ocurre otro error, lo mostramos en la consola
        print(error)
    
    # Redirigimos a la lista de usuarios
    return redirect('lista_usuarios')





# Vista para crear un nuevo juego
def crear_juego(request):
    datosFormulario = None  # Inicializamos la variable para los datos del formulario

    if request.method == "POST":
        datosFormulario = request.POST  # Capturamos los datos enviados por el formulario
    
    # Creamos el formulario con los datos recibidos
    formulario = JuegoForm(datosFormulario)

    if request.method == "POST":
        if formulario.is_valid():  # Validamos el formulario
            try:
                # Guardamos el juego en la base de datos
                formulario.save()
                # Mostramos un mensaje de éxito
                messages.success(request, "El juego ha sido creado correctamente.")
                return redirect("lista_juegos")  # Redirigimos a la lista de juegos
            except Exception as error:
                print(error)  # Imprimimos el error en la consola para depuración

    return render(request, 'torneo/crearjuego/crear_juego.html', {'formulario': formulario})



def lista_juegos(request):
    # Obtener todos los juegos de la base de datos
    juegos = Juego.objects.all()
    
    # Renderizar la plantilla y pasar los juegos como contexto
    return render(request, 'torneo/lista_juegos.html', {'juegos': juegos})

def juego_buscar_avanzado(request):
    if len(request.GET) > 0:
        formulario = BusquedaJuegoForm(request.GET)
        if formulario.is_valid():
            mensaje_busqueda = "Se ha buscado por los siguientes valores:\n"
            
            QJuegos = Juego.objects.prefetch_related("torneos")
            
            # Obtenemos los filtros del formulario
            nombre = formulario.cleaned_data.get('nombre')
            genero = formulario.cleaned_data.get('genero')
            descripcion = formulario.cleaned_data.get('descripcion')
   
            if nombre:
                QJuegos = QJuegos.filter(nombre__icontains=nombre)
                mensaje_busqueda += f" Nombre que contenga la palabra '{nombre}'\n"
            
            if genero:
                QJuegos = QJuegos.filter(genero__icontains=genero)
                mensaje_busqueda += f" Género que contenga la palabra '{genero}'\n"
            
            if descripcion:
                QJuegos = QJuegos.filter(descripcion__icontains=descripcion)
                mensaje_busqueda += f" Descripción que contenga la palabra '{descripcion}'\n"
            
            
            # Ejecutamos la consulta
            juegos = QJuegos.all()

            if not juegos.exists():
                messages.info(request, 'No se encontraron juegos con los filtros aplicados.')

            return render(request, 'torneo/crearjuego/buscar_juego.html', {
                "juegos_mostrar": juegos,
                "texto_busqueda": mensaje_busqueda
            })
    else:
        formulario = BusquedaJuegoForm(None)
    
    return render(request, 'torneo/crearjuego/busqueda_avanzada.html', {"formulario": formulario})





def juego_editar(request, juego_id):
    # Obtenemos el juego correspondiente al ID proporcionado
    juego = Juego.objects.get(id=juego_id)  
    
    datosFormulario = None  # Inicializamos la variable para los datos del formulario

    if request.method == "POST":
        datosFormulario = request.POST  # Capturamos los datos enviados por el formulario
    
    # Creamos el formulario usando la instancia del juego actual
    formulario = JuegoForm(datosFormulario, instance=juego)
    
    if request.method == "POST":
        if formulario.is_valid():  # Validamos el formulario
            try:
                # Guardamos los cambios en la base de datos
                formulario.save()
                # Mostramos un mensaje de éxito
                messages.success(
                    request,
                    f"Se ha editado el juego '{formulario.cleaned_data.get('nombre')}' correctamente."
                )
                return redirect('lista_juegos')  # Redirigimos a la lista de juegos
            except Exception as error:
                print(error)  # Imprimimos el error en la consola para depuración
    
    # Renderizamos el formulario de edición
    return render(
        request,
        'torneo/crearjuego/crear_juego.html',  
        {"formulario": formulario, "juego": juego}
    )


def juego_eliminar(request, juego_id):
    try:
        # Obtenemos el juego correspondiente al ID proporcionado
        juego = Juego.objects.get(id=juego_id)
        
        # Eliminamos el juego
        juego.delete()
        
        # Mostramos un mensaje de éxito
        messages.success(request, f"Se ha eliminado el juego {juego.nombre} correctamente.")
        
    except Juego.DoesNotExist:
        # Si el juego no existe, mostramos un mensaje de error
        messages.error(request, "El juego no existe.")
    except Exception as error:
        # Si ocurre otro error, lo mostramos en la consola
        print(error)
    
    # Redirigimos a la lista de juegos
    return redirect('lista_juegos')


def crear_perfil_de_jugador(request):
    datosFormulario = None  # Inicializamos la variable para los datos del formulario

    if request.method == "POST":
        datosFormulario = request.POST  # Capturamos los datos enviados por el formulario
    
    # Creamos el formulario
    formulario = PerfilDeJugadorForm(datosFormulario)

    if request.method == "POST":
        if formulario.is_valid():  # Validamos el formulario
            try:
                # Guardamos el perfil de jugador en la base de datos
                formulario.save()
                # Mostramos un mensaje de éxito
                messages.success(request, "El perfil de jugador ha sido creado correctamente.")
                return redirect("lista_perfiles_de_jugadores")  # Redirigimos a la lista de perfiles de jugadores
            except Exception as error:
                print(error)  # Imprimimos el error en la consola para depuración

    return render(request, 'torneo/crearperfil/crear_perfil_de_jugador.html', {'formulario': formulario})

def perfil_buscar_avanzado(request):
    if len(request.GET) > 0:
        formulario = BusquedaAvanzadaPerfilJugadorForm(request.GET)
        if formulario.is_valid():
            mensaje_busqueda = "Se ha buscado por los siguientes valores:\n"
            
            QPerfiles = PerfilDeJugador.objects.select_related("usuario")
            
            # Obtenemos los filtros del formulario
            textoBusqueda = formulario.cleaned_data.get('textoBusqueda')
            puntos_minimos = formulario.cleaned_data.get('puntos_minimos')
            nivel_minimo = formulario.cleaned_data.get('nivel_minimo')
            
            # Aplicamos los filtros según corresponda
            if textoBusqueda:
                QPerfiles = QPerfiles.filter(usuario__nombre__icontains=textoBusqueda)
                mensaje_busqueda += f" Nombre que contenga la palabra '{textoBusqueda}'\n"
            
            if puntos_minimos is not None:
                QPerfiles = QPerfiles.filter(puntos__gte=puntos_minimos)
                mensaje_busqueda += f" Puntos mayores o iguales a {puntos_minimos}\n"
            
            if nivel_minimo is not None:
                QPerfiles = QPerfiles.filter(nivel__gte=nivel_minimo)
                mensaje_busqueda += f" Nivel mayor o igual a {nivel_minimo}\n"
            
            # Ejecutamos la consulta
            perfiles = QPerfiles.all()

            if not perfiles.exists():
                messages.info(request, 'No se encontraron perfiles con los filtros aplicados.')

            return render(request, 'torneo/crearperfil/buscar_perfil.html', {
                "perfiles_mostrar": perfiles,
                "texto_busqueda": mensaje_busqueda
            })
    else:
        formulario = BusquedaAvanzadaPerfilJugadorForm(None)
    
    return render(request, 'torneo/crearperfil/busqueda_avanzada.html', {"formulario": formulario})




def lista_perfiles(request):
    # Obtener todos los perfiles de jugadores de la base de datos
    perfiles = PerfilDeJugador.objects.all()
    
    return render(request, 'torneo/lista_perfiles.html', {'perfiles': perfiles})



def perfil_editar(request, perfil_id):
    # Obtenemos el perfil de jugador correspondiente al ID proporcionado
    perfil = PerfilDeJugador.objects.get(id=perfil_id)  
    
    datosFormulario = None  # Inicializamos la variable para los datos del formulario

    if request.method == "POST":
        datosFormulario = request.POST  # Capturamos los datos enviados por el formulario
    
    # Creamos el formulario usando la instancia del perfil de jugador actual
    formulario = PerfilDeJugadorForm(datosFormulario, instance=perfil)
    
    if request.method == "POST":
        if formulario.is_valid():  # Validamos el formulario
            try:
                # Guardamos los cambios en la base de datos
                formulario.save()
                # Mostramos un mensaje de éxito
                messages.success(
                    request,
                    f"Se ha editado el perfil de '{formulario.cleaned_data.get('usuario')}' correctamente."
                )
                return redirect('lista_perfiles')  # Redirigimos a la lista de perfiles
            except Exception as error:
                print(error)  # Imprimimos el error en la consola para depuración
    
    # Renderizamos el formulario de edición
    return render(
        request,
        'torneo/crearperfil/crear_perfil_de_jugador.html', 
        {"formulario": formulario, "perfil": perfil}
    )

def perfil_eliminar(request, perfil_id):
    try:
        # Obtenemos el perfil correspondiente al ID proporcionado
        perfil = PerfilDeJugador.objects.get(id=perfil_id)
        
        # Eliminamos el perfil
        perfil.delete()
        
        # Mostramos un mensaje de éxito
        messages.success(request, f"Se ha eliminado el perfil de jugador {perfil.usuario.username} correctamente.")
        
    except PerfilDeJugador.DoesNotExist:
        # Si el perfil no existe, mostramos un mensaje de error
        messages.error(request, "El perfil de jugador no existe.")
    except Exception as error:
        # Si ocurre otro error, lo mostramos en la consola
        print(error)
    
    # Redirigimos a la lista de perfiles
    return redirect('lista_perfiles') 



def registrar_usuario(request):
    if request.method == 'POST':
        formulario = RegistroForm(request.POST)
        if formulario.is_valid():
            user = formulario.save()  # Guardamos el usuario creado
            
            rol = int(formulario.cleaned_data.get('rol'))  # Obtenemos el rol elegido
            
            # Asignamos el rol y lo añadimos al grupo correspondiente
            if rol == UsuarioLogin.ADMINISTRADOR:
                grupo = Group.objects.get(name='Administradores') 
                grupo.user_set.add(user)
            elif rol == UsuarioLogin.JUGADOR:
                grupo = Group.objects.get(name='Jugadores') 
                grupo.user_set.add(user)
                jugador = Jugador.objects.create(usuario=user, puntos=0)
                jugador.save()
            elif rol == UsuarioLogin.ORGANIZADOR:
                grupo = Group.objects.get(name='Organizadores') 
                grupo.user_set.add(user)
                organizador = Organizador.objects.create(usuario=user, eventos_creados=0)
                organizador.save()

            login(request, user)  # Hacemos login al usuario recién registrado
            return redirect('index')  # Redirigimos a la página principal (o cualquier vista que desees)
    else:
        formulario = RegistroForm()  # Creamos una instancia del formulario vacío
    
    return render(request, 'torneo/registration/signup.html', {'formulario': formulario})  # Renderizamos la página de registro






#Distintos errores de las paginas web
def mi_error_404(request, exception=None):
    return render(request, 'torneo/errores/404.html', None,None,404)
def mi_error_400(request, exception=None):
    return render(request, 'torneo/errores/400.html', None,None,400)
def mi_error_403(request, exception=None):
    return render(request, 'torneo/errores/403.html', None,None,403)
def mi_error_500(request, exception=None):
    return render(request, 'torneo/errores/403.html', None,None,500)

