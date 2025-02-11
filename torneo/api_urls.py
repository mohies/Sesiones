from django.urls import path
from . import api_views  # Asegúrate de importar las vistas correctas
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('torneos/', api_views.torneo_list_sencillo, name='torneo-list-sencillo'),

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
    



]
