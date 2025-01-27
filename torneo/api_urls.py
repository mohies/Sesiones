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
    
    
    

]
