from django.contrib import admin
from .models import *
	
# Register your models here.
models = [Usuario, PerfilDeJugador, Torneo,Consola,Juego,Participante,Espectador,Equipo,Clasificacion,ParticipanteEquipo,TorneoJuego,TorneoParticipante]

# Registro de modelos en el admin
for model in models:    
    admin.site.register(model)