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
    
    participantes = forms.ModelMultipleChoiceField(
        queryset=Participante.objects.all(),
        required=True,
        widget=forms.CheckboxSelectMultiple(),
        help_text="Selecciona los participantes del torneo"
    )
    
    duracion = forms.ChoiceField(
        label="Duración del Torneo",
        choices=DURACIONES,
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'}),
        help_text="Selecciona la duración del torneo"
    )
    
    
    
    class Meta:
        model = Torneo  # Asociamos el formulario al modelo Torneo
        fields = ['nombre', 'descripcion', 'fecha_inicio', 'categoria', 'participantes', 'duracion']# Campos que se mostrarán en el formulario
        widgets = {

            'fecha_inicio': forms.DateInput(format="%Y-%m-%d",attrs={'type': 'date', 'class': 'form-control'})
        }
        

    def clean(self):
        super().clean() #se llama al clean ejecutan las validaciones 
        #predefinidas de Django (como asegurarse de que los campos requeridos estén presentes, que los campos numéricos sean válidos, etc.), 
        #y luego se devuelve un diccionario cleaned_data con los valores validados de los campos.

        #una vez calidado accedemos a los valores del clean y ya luego podemos añadir nuestros propios errores
        nombre = self.cleaned_data.get('nombre')
        descripcion = self.cleaned_data.get('descripcion')
        fecha_inicio = self.cleaned_data.get('fecha_inicio')
        categoria = self.cleaned_data.get('categoria')
        participantes = self.cleaned_data.get('participantes')
        duracion = self.cleaned_data.get('duracion')
        
            # Asegurarnos de que duracion esté en formato timedelta
        if isinstance(duracion, str):  # Si la duración es una cadena de texto, la convertimos a timedelta
            horas, minutos = map(int, duracion.split(':'))
            duracion = timedelta(hours=horas, minutes=minutos)

        # Validaciones personalizadas (como las tenías)
            torneoNombre = Torneo.objects.filter(nombre=nombre).first()
            if(not torneoNombre is None
            ):
                if(not self.instance is None and torneoNombre.id == self.instance.id):
                    pass
                else:
                    self.add_error('nombre','Ya existe un torneo con ese nombre')

        if descripcion and len(descripcion) < 20:
            self.add_error('descripcion', 'La descripción debe tener al menos 20 caracteres.')

        if fecha_inicio and fecha_inicio < date.today():
            self.add_error('fecha_inicio', 'La fecha de inicio no puede ser anterior a hoy.')
        # Comprobamos que la categoría sea 'Acción' y que la duración supere las 3 horas (10800 segundos)
        if categoria and categoria.lower() == "acción":
            if duracion:
                # Verifica si la duración es mayor a 3 horas (10800 segundos)
                if isinstance(duracion, timedelta) and duracion.total_seconds() > 10800:
                    self.add_error('categoria', 'La categoría "Acción" no puede tener una duración superior a 3 horas.')
                    self.add_error('duracion', 'Duración no válida para la categoría "Acción".')

                return self.cleaned_data


        if participantes and len(participantes) < 2:
            self.add_error('participantes', 'Debe seleccionar al menos dos participantes.')

        return self.cleaned_data

    
    
class BusquedaTorneoForm(forms.Form):
    textoBusqueda = forms.CharField(required=True)
    
    
class BusquedaAvanzadaTorneoForm(forms.Form):
    textoBusqueda = forms.CharField(required=False)
    
    
    categorias = forms.CharField(
    required=False,
    widget=forms.TextInput(attrs={'placeholder': 'Introduce las categorías separadas por comas'})
)

    fecha_desde = forms.DateField(label="Fecha Desde", 
                                  required=False, 
                                  widget=forms.DateInput(attrs={"type": "date", "class": "form-control"}))

    fecha_hasta = forms.DateField(label="Fecha Hasta", 
                                  required=False,
                                  initial=datetime.date.today,
                                  widget=forms.DateInput(format="%Y-%m-%d", 
                                                         attrs={"type": "date", "class": "form-control"}))

    # Filtrar por duración mínima de los torneos
    duracion_minima = forms.TimeField(label="Duración mínima", 
                                      required=False, 
                                      widget=forms.TimeInput(attrs={"type": "time", "class": "form-control"}))
    


    def clean(self):
        # Validamos con el formulario base
        super().clean()

        # Obtenemos los campos
        textoBusqueda = self.cleaned_data.get('textoBusqueda')
        fecha_desde = self.cleaned_data.get('fecha_desde')
        fecha_hasta = self.cleaned_data.get('fecha_hasta')
        duracion_minima = self.cleaned_data.get('duracion_minima')

        # Controlamos que al menos se haya introducido un valor en uno de los campos
        if not textoBusqueda and not fecha_desde and not fecha_hasta and not duracion_minima:
            error_message = 'Debe introducir al menos un valor en un campo del formulario'
            self.add_error('textoBusqueda', error_message)
            self.add_error('fecha_desde', error_message)
            self.add_error('fecha_hasta', error_message)
            self.add_error('duracion_minima', error_message)
            # Validar que el texto de búsqueda tenga al menos 3 caracteres si se ingresa algo
        if textoBusqueda != "" and len(textoBusqueda) < 3:
                self.add_error('textoBusqueda', 'Debe introducir al menos 3 caracteres')

            # La fecha hasta debe ser mayor o igual a la fecha desde, si ambas se introducen
        if fecha_desde and fecha_hasta and fecha_hasta < fecha_desde:
                self.add_error('fecha_desde', 'La fecha hasta no puede ser menor que la fecha desde')
                self.add_error('fecha_hasta', 'La fecha hasta no puede ser menor que la fecha desde')

            # Si se especifica una duración mínima, debe ser un tiempo positivo
        if duracion_minima:
            if duracion_minima.total_seconds() <= 0:
                self.add_error('duracion_minima', 'La duración mínima debe ser un tiempo válido y mayor que cero')

        # Siempre devolvemos el conjunto de datos
        return self.cleaned_data


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

        




    



   
