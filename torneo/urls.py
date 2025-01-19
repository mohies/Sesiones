from django.urls import path
from . import views
from django.contrib.auth.views import LoginView,LogoutView
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.index, name='index'),
    path('lista',views.lista_torneo,name='lista_torneo'),
    path('crear-torneo/', views.crear_torneo, name='crear_torneo'),
    path('buscar_torneo/', views.torneo_buscar_avanzado, name='buscar_torneo'),
    path('registro/', views.registrar_usuario, name='registro'),
    path('crear/', views.torneo_crear, name='torneo_crear'),
    path('editar/<int:torneo_id>/', views.torneo_editarr, name='torneo_editarr'),
    path('eliminar/<int:torneo_id>/', views.torneo_eliminar, name='torneo_eliminar'),
    path('ver/<int:torneo_id>/', views.torneo_ver, name='torneo_ver'),
     # Ruta para login
    path('login/', LoginView.as_view(template_name='torneo/registration/login.html'), name='login'),
    
    # Ruta para logout
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('torneo/jugador/', views.torneo_jugador, name='torneo_jugador'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),








]
