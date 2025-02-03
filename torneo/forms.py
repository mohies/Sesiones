from django import forms  # Importa el módulo de formularios
from django.forms import ModelForm  # Importa ModelForm directamente
from .models import *
from datetime import datetime, date, timedelta
from django.forms import DateInput
import datetime
from django.contrib.auth.forms import UserCreationForm
from .models import UsuarioLogin  # Usamos UsuarioLogin ya que es el modelo que define el rol

class TorneoForm(forms.ModelForm):
    DURACIONES = [
        ('1:00', '1 hora'),
        ('2:00', '2 horas'),
        ('3:00', '3 horas'),
        ('4:00', '4 horas'),
        ('5:00', '5 horas'),
        ('6:00', '6 horas'),
        ('12:00', '12 horas'),
        ('24:00', '1 día'),
    ]
    
    CATEGORIAS = [
        ('Acción', 'Acción'),
        ('Deportes', 'Deportes'),
        ('Aventura', 'Aventura'),
        ('Estrategia', 'Estrategia'),
    ]
    
    categoria = forms.ChoiceField(
        label="Categoría",
        choices=CATEGORIAS,
        required=True,
        help_text="Selecciona la categoría del torneo (por ejemplo, 'Acción', 'Deportes', etc.)"
    )
    
    duracion = forms.ChoiceField(
        label="Duración del Torneo",
        choices=DURACIONES,
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'}),
        help_text="Selecciona la duración del torneo"
    )

    jugadores = forms.ModelMultipleChoiceField(
        queryset=Jugador.objects.all(),  # Todos los jugadores disponibles
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Jugadores asociados al torneo"
    )

    class Meta:
        model = Torneo
        fields = ['nombre', 'descripcion', 'fecha_inicio', 'categoria', 'duracion', 'jugadores']  # Añadido 'jugadores'

        widgets = {
            'fecha_inicio': forms.DateInput(format="%Y-%m-%d", attrs={'type': 'date', 'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:  # Si estamos editando un torneo ya existente
            # Establecer los jugadores seleccionados inicialmente
            self.fields['jugadores'].initial = self.instance.jugadores.all()

    def clean(self):
        super().clean()

        nombre = self.cleaned_data.get('nombre')
        descripcion = self.cleaned_data.get('descripcion')
        fecha_inicio = self.cleaned_data.get('fecha_inicio')
        categoria = self.cleaned_data.get('categoria')
        duracion = self.cleaned_data.get('duracion')

        if isinstance(duracion, str):  # Convertir la duración en timedelta si es necesario
            horas, minutos = map(int, duracion.split(':'))
            duracion = timedelta(hours=horas, minutes=minutos)

        # Validación de nombre único
        torneo_nombre = Torneo.objects.filter(nombre=nombre).first()
        if torneo_nombre and (not self.instance or torneo_nombre.id != self.instance.id):
            self.add_error('nombre', 'Ya existe un torneo con ese nombre')

        if descripcion and len(descripcion) < 20:
            self.add_error('descripcion', 'La descripción debe tener al menos 20 caracteres.')

        if fecha_inicio and fecha_inicio < date.today():
            self.add_error('fecha_inicio', 'La fecha de inicio no puede ser anterior a hoy.')

        # Validaciones adicionales para categorías y duraciones
        if categoria and categoria.lower() == "acción":
            if duracion and isinstance(duracion, timedelta) and duracion.total_seconds() > 10800:
                self.add_error('categoria', 'La categoría "Acción" no puede tener una duración superior a 3 horas.')
                self.add_error('duracion', 'Duración no válida para la categoría "Acción".')

        return self.cleaned_data


    
    
class BusquedaTorneoForm(forms.Form):
    textoBusqueda = forms.CharField(required=True)
    
class BusquedaAvanzadaTorneoForm(forms.Form):
    textoBusqueda = forms.CharField(required=False)
    fecha_desde = forms.DateField(required=False, widget=forms.DateInput(attrs={"type": "date"}))
    fecha_hasta = forms.DateField(required=False, widget=forms.DateInput(attrs={"type": "date"}))
    categoria = forms.CharField(required=False)

class BusquedaAvanzadaEquipoForm(forms.Form):
    nombre = forms.CharField(required=False)
    fecha_ingreso_desde = forms.DateField(required=False, widget=forms.DateInput(attrs={"type": "date"}))
    fecha_ingreso_hasta = forms.DateField(required=False, widget=forms.DateInput(attrs={"type": "date"}))
    puntos_contribuidos_min = forms.IntegerField(required=False)

class BusquedaAvanzadaParticipanteForm(forms.Form):
    nombre = forms.CharField(required=False)
    puntos_obtenidos_min = forms.IntegerField(required=False)
    fecha_inscripcion_desde = forms.DateField(required=False, widget=forms.DateInput(attrs={"type": "date"}))
    fecha_inscripcion_hasta = forms.DateField(required=False, widget=forms.DateInput(attrs={"type": "date"}))

class BusquedaAvanzadaJuegoForm(forms.Form):
    nombre = forms.CharField(required=False)
    genero = forms.CharField(required=False)
    fecha_participacion_desde = forms.DateField(required=False, widget=forms.DateInput(attrs={"type": "date"}))
    fecha_participacion_hasta = forms.DateField(required=False, widget=forms.DateInput(attrs={"type": "date"}))

class RegistroForm(UserCreationForm):
    roles = (
        (UsuarioLogin.JUGADOR, 'Jugador'),
        (UsuarioLogin.ORGANIZADOR, 'Organizador'),
    )

    rol = forms.ChoiceField(choices=roles, label="Rol", required=True)

    class Meta:
        model = UsuarioLogin
        fields = ('username', 'email', 'password1', 'password2', 'rol')


class RegistroJugadorForm(forms.ModelForm):
    class Meta:
        model = Jugador
        fields = ['puntos', 'equipo']


class RegistroOrganizadorForm(forms.ModelForm):
    class Meta:
        model = Organizador
        fields = ['eventos_creados']


class TorneoJugadorForm(forms.Form):
    # Definimos un campo Select para seleccionar un torneo relacionado con el jugador
    torneos_disponibles = Torneo.objects.all()
    torneo = forms.ModelChoiceField(
        queryset=torneos_disponibles,
        widget=forms.Select,
        required=True,
        empty_label="Seleccione un torneo"
    )











