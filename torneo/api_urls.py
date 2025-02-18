from django.urls import path,include
from . import api_views  # Asegúrate de importar las vistas correctas
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter
from .viewsets import TorneoViewSet  # Importamos el ViewSet
router = DefaultRouter()
router.register(r'to', TorneoViewSet, basename='torneo')

urlpatterns = [
    ##path('torneos/', api_views.torneo_list_sencillo, name='torneo-list-sencillo'),

    # Ruta para la vista de torneos (consulta mejorada) usando "/api/v1/torneos/mejorada/"
    path('torneos/mejorada/', api_views.torneo_list, name='torneo_list'),
    path('equipos/', api_views.equipo_list_sencillo, name='equipo-list-sencillo'),
    path('participantes/mejorada/', api_views.participante_list_mejorado, name='participante-list-mejorada'),
    path('juegos/mejorada/', api_views.juego_list_mejorado, name='juego-list-mejorada'),
    
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Obtener el token
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Refrescar el token
    
    path('torneos/buscar/', api_views.torneo_buscar, name='torneo_buscar'),
    path('torneos/buscar/avanzado/', api_views.torneo_buscar_avanzado, name='torneo_buscar_avanzado'),
    path('equipos/buscar/avanzado/', api_views.equipo_buscar_avanzado, name='equipo_buscar_avanzado'),
    path('participantes/buscar/avanzado/', api_views.participante_buscar_avanzado, name='participante_buscar_avanzado'),
    path('juegos/buscar/avanzado/', api_views.juego_buscar_avanzado, name='juego_buscar_avanzado'),
    path('categorias/', api_views.categoria_list, name='categoria_list'),
    path('participantes/', api_views.participante_list, name='participante_list'),
    path('torneos/crear/', api_views.torneo_create, name='torneo_create'),
    path('torneos/editar/<int:torneo_id>/', api_views.torneo_editar, name='torneo_editar'),
    path('torneos/<int:torneo_id>/', api_views.torneo_obtener, name='torneo_obtener'),
    path('torneos/actualizar-nombre/<int:torneo_id>/', api_views.torneo_actualizar_nombre, name='torneo_actualizar_nombre'),
    path('torneos/eliminar/<int:torneo_id>/', api_views.torneo_eliminar, name='torneo_eliminar'),
    path('torneos_list/', api_views.torneo_list, name='torneo_list'),
    path('consolas/', api_views.consola_list, name='consola_list'),
    path('juegos/crear/', api_views.juego_create, name='juego_create'),
    path('juegos/<int:juego_id>/', api_views.juego_obtener, name='juego_obtener'),
    path('juegos/editar/<int:juego_id>/', api_views.juego_editar, name='juego_editar'),
    path('juegos/actualizar-nombre/<int:juego_id>/', api_views.juego_actualizar_nombre, name='juego_actualizar_nombre'),
    path('juegos/eliminar/<int:juego_id>/', api_views.juego_eliminar, name='juego_eliminar'),
    path('usuarios/', api_views.usuario_list, name='usuario_list'),
    path('equipos/', api_views.equipo_list, name='equipo_list'),
    path('participantes/crear/', api_views.participante_create, name='participante_create'),
    path('participantes/<int:participante_id>/', api_views.participante_obtener, name='participante_obtener'),
    path('participantes/editar/<int:participante_id>/', api_views.participante_editar, name='participante_editar'),
    path('participantes/actualizar-equipos/<int:participante_id>/', api_views.participante_actualizar_equipos, name='participante_actualizar_equipos'),
    path('participantes/eliminar/<int:participante_id>/', api_views.participante_eliminar, name='participante_eliminar'),
    path('usuarios-login/', api_views.usuariologin_list, name='usuariologin_list'),  # La URL debe coincidir con la del helper
    path('jugadores/crear/', api_views.jugador_create, name='jugador_crear'),
    path('jugadores/obtener/<int:jugador_id>/', api_views.jugador_obtener, name='jugador_obtener'),
    path('jugadores/editar/<int:jugador_id>/', api_views.jugador_editar, name='jugador_editar'),
    path('jugadores/actualizar_puntos/<int:jugador_id>/', api_views.jugador_actualizar_puntos, name="jugador_actualizar_puntos"),
    path('jugadores/eliminar/<int:jugador_id>/<int:torneo_id>/', api_views.jugador_eliminar_torneo, name="jugador_eliminar_torneo"),

     path('', include(router.urls)),








    


    



]
