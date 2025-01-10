from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('lista',views.lista_torneo,name='lista_torneo'),
    path('crear-torneo/', views.crear_torneo, name='crear_torneo'),
    path('crear-equipo/', views.crear_equipo, name='crear_equipo'),  # Nueva ruta para crear equipo
    path('buscar_torneo/', views.torneo_buscar_avanzado, name='buscar_torneo'),
    path('torneo/editar/<int:torneo_id>/', views.torneo_editar, name='torneo_editar'),
    path('torneo/eliminar/<int:torneo_id>/', views.torneo_eliminar, name='torneo_eliminar'),
    path('buscar_equipo/', views.equipo_buscar_avanzado, name='buscar_equipo'),
    path('lista_equipo/',views.lista_equipos,name='lista_equipos'),
    path('equipo/editar/<int:equipo_id>/', views.equipo_editar, name='equipo_editar'),
    path('equipo/eliminar/<int:equipo_id>/', views.equipo_eliminar, name='equipo_eliminar'),
    path('crear-participante/', views.crear_participante, name='crear_participante'),
    path('buscar_participante/', views.participante_buscar_avanzado, name='buscar_participante'),
    path('lista_participantes/',views.lista_participantes,name='lista_participantes'),
    path('participante/editar/<int:participante_id>/', views.participante_editar, name='participante_editar'),
    path('participante/eliminar/<int:participante_id>/', views.participante_eliminar, name='participante_eliminar'),
    path('usuario/crear/', views.crear_usuario, name='crear_usuario'),
    path('buscar-usuario/', views.usuario_buscar_avanzado, name='buscar_usuario'),
    path('usuarios/', views.lista_usuarios, name='lista_usuarios'),
    path('editar_usuario/<int:usuario_id>/', views.usuario_editar, name='usuario_editar'),
    path('usuario/eliminar/<int:usuario_id>/', views.usuario_eliminar, name='usuario_eliminar'),
    path('crearjuego/', views.crear_juego, name='crear_juego'),
    path('juegos/', views.lista_juegos, name='lista_juegos'),
    path('buscar-juego/', views.juego_buscar_avanzado, name='buscar_juego'),
    path('juego/editar/<int:juego_id>/', views.juego_editar, name='juego_editar'),
    path('juego/eliminar/<int:juego_id>/', views.juego_eliminar, name='juego_eliminar'),
    path('crear_perfil_de_jugador/', views.crear_perfil_de_jugador, name='crear_perfil_de_jugador'),
    path('perfiles/', views.lista_perfiles, name='lista_perfiles'),
    path('buscar-perfil/', views.perfil_buscar_avanzado, name='buscar_perfil'),
    path('perfil/editar/<int:perfil_id>/', views.perfil_editar, name='editar_perfil'),
    path('perfil/eliminar/<int:perfil_id>/', views.perfil_eliminar, name='eliminar_perfil'),
    path('registro/', views.registrar_usuario, name='registro'),
    path('crear/', views.torneo_crear_generico_con_request, name='torneo_crear'),
    path('editar/<int:torneo_id>/', views.torneo_editar_generico_con_request, name='torneo_editar'),
    path('eliminar/<int:torneo_id>/', views.torneo_eliminar, name='torneo_eliminar'),
    path('ver/<int:torneo_id>/', views.torneo_ver, name='torneo_ver'),







]
