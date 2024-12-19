from datetime import date
from django import forms
from oferta.models import Oferta
from usuario.models import Usuario
from oferente.models import Oferente
from persona.models import Persona
from django import forms
from django.contrib.auth import authenticate
from django_recaptcha.fields import ReCaptchaField
from proyecto_descuentos2.settings import RECAPTCHA_PUBLIC_KEY, RECAPTCHA_PRIVATE_KEY
from django import forms

from django import forms
from usuario.models import Usuario
from django import forms
from .models import ConfiguracionSistema

from django import forms
from .models import ConfiguracionSistema

from django import forms
from .models import ConfiguracionSistema

class ConfiguracionSistemaForm(forms.ModelForm):
    FORMATOS_IMAGEN_CHOICES = [
        ('jpg', 'JPG'),
        ('png', 'PNG'),
        ('gif', 'GIF'),
        ('bmp', 'BMP'),
        ('webp', 'WebP'),
    ]

    # Opciones predefinidas para cantidad de ofertas
    CANTIDAD_OFERTAS_CHOICES = [
        (3, '3 ofertas'),
        (5, '5 ofertas'),
        (10, '10 ofertas'),
        (15, '15 ofertas'),
        (20, '20 ofertas'),
    ]

    formatos_imagen_permitidos = forms.MultipleChoiceField(
        choices=FORMATOS_IMAGEN_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        label="Formatos de imagen permitidos",
        help_text="Selecciona los formatos de imagen permitidos.",
    )

    cantidad_maxima_ofertas = forms.ChoiceField(
        choices=CANTIDAD_OFERTAS_CHOICES,
        label="Cantidad máxima de ofertas",
        widget=forms.Select(attrs={'class': 'form-select'}),
    )

    class Meta:
        model = ConfiguracionSistema
        fields = ['cantidad_maxima_ofertas', 'formatos_imagen_permitidos']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            # Si la instancia existe, carga los formatos guardados y los convierte en lista
            self.initial['formatos_imagen_permitidos'] = self.instance.formatos_imagen_permitidos.split(",")

    def save(self, commit=True):
        # Al guardar, convierte la lista en una cadena separada por comas
        instance = super().save(commit=False)
        instance.formatos_imagen_permitidos = ",".join(self.cleaned_data['formatos_imagen_permitidos'])
        if commit:
            instance.save()
        return instance



    
    
class SuperUsuarioForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirmar Contraseña")

    class Meta:
        model = Usuario
        fields = ['username', 'email', 'telefono']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return cleaned_data







class LoginSuperuserForm(forms.Form):
    username = forms.CharField(
        label="Nombre de Usuario",
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de Usuario'}),
    )
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}),
    )


    captcha  =  ReCaptchaField ( 
        label='',
        public_key =RECAPTCHA_PUBLIC_KEY, 
        private_key = RECAPTCHA_PRIVATE_KEY,
    )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        user = authenticate(username=username, password=password)

        if user is None:
            raise forms.ValidationError("Nombre de usuario o contraseña incorrectos.")

        if not (user.is_superuser and user.is_staff):
            raise forms.ValidationError("No tienes permisos para acceder al panel.")

        # Guarda el usuario autenticado en cleaned_data
        cleaned_data['user'] = user
        return cleaned_data



class UsuarioForm(forms.ModelForm):
    persona = forms.ModelChoiceField(
        # usuario__isnull=True, eliminado=Falseasegura que solo se muestren personas que no están asociadas a
        #  un usuario y que no están eliminadas.
        queryset=Persona.objects.filter(usuario__isnull=True, eliminado=False),
        required=True,
        label="Persona asociada",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    class Meta:
        model = Usuario
        fields = ['username', 'email', 'is_active','persona',]
        labels = {
            'username': 'Nombre de usuario',
            'email': 'Correo Electrónico',
            'is_active': '¿Activo?',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el nombre de usuario'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el correo electrónico'}),
            'is_active': forms.RadioSelect(choices=[(True, 'Sí'), (False, 'No')]),
        }

    def save(self, commit=True):
        usuario = super().save(commit=False)
        # Asocia la persona seleccionada al usuario
        persona = self.cleaned_data.get('persona')
        if persona:
            usuario.persona_id = persona
        if commit:
            usuario.save()
        return usuario
    
class PersonForm(forms.ModelForm):
    class Meta:
        model = Persona
        fields = ('identificacion', 'nombres', 'apellidos')  # Personaliza los campos según tus necesidades
        widgets = {
            'identificacion': forms.TextInput(attrs={'class': 'form-control',
                                                     'placeholder': ' Ingrese su DNI (sin puntos)',
                                                     'min': '1000000',
                                                     'autocomplete': 'off'}),
            'nombres': forms.TextInput(attrs={'class': 'form-control',
                                              'placeholder': 'Ingrese su nombre completo','autocomplete': 'off'}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control',
                                                'placeholder': ' Ingrese su apellido/s','autocomplete': 'off'})
        }
    def __init__(self, *args, **kwargs):
        super(PersonForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] += ' mb-2'  # Añadir espacio entre los campos si es necesario
            field.label_tag = lambda label, attrs={}, field_id=None: (
                label and label % field.label or ''
            )
    
     #VALIDACIONES

    #validacion de contraseña: el valor ingresado no puede ser menor a 1000000
    def clean_identificacion(self):
        identificacion = self.cleaned_data.get('identificacion')
        if identificacion < 1000000:
            raise forms.ValidationError('Debes ingresar un número de DNI superior a 1000000')
        return identificacion


class ComercioForm(forms.ModelForm):
    class Meta:
        model = Oferente
        fields = ['nombrecomercio', 'cuit', 'habilitado']
        labels = {
            'nombrecomercio': 'Nombre del comercio',
            'cuit': 'Cuit del comercio',
            'habilitado': '¿Activo?',
        }
        widgets = {
            'nombrecomercio': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el nombre del comercio'}),
            'cuit': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el correo electrónico'}),
            'habilitado': forms.RadioSelect(choices=[(True, 'Sí'), (False, 'No')]),
        }



class OfertaForm(forms.ModelForm):
    
    oferente = forms.ModelChoiceField(
        queryset=Oferente.objects.none(),  # Inicialmente vacío, se llenará en el __init__
        widget=forms.Select,
        required=True,
        label="Oferente"
    )

    class Meta:
        model = Oferta
        fields = ['titulo', 'descripcion', 'precio_normal', 'precio_oferta', 'oferente', 'fecha_inicio', 'fecha_fin', 'imagen']
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date'}),
            'fecha_fin': forms.DateInput(attrs={'type': 'date'}),
            'precio_normal':forms.NumberInput(attrs={'step': '0.01', 'class': 'form-control', 'required': ''}),
            'precio_oferta':forms.NumberInput(attrs={'step': '0.01', 'class': 'form-control', 'required': ''})
            
        }
    
    def clean(self):
        cleaned_data = super().clean()
        fecha_inicio = cleaned_data.get("fecha_inicio")
        fecha_fin = cleaned_data.get("fecha_fin")

        # Verificá que ambas fechas estén presentes
        if fecha_inicio and fecha_fin:
            # Comprobá que la fecha de inicio sea anterior o igual a la de fin
            if fecha_inicio > fecha_fin:
                raise forms.ValidationError("La fecha de inicio no puede ser posterior a la fecha de fin.")
            # Comprobá que la fecha de inicio sea hoy o en el futuro
            if fecha_inicio < date.today():
                raise forms.ValidationError("La fecha de inicio debe ser hoy o una fecha futura.")

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Obtener el usuario del argumento kwargs
        super().__init__(*args, **kwargs)

        # Filtrar los comercios asociados al usuario
        if user is not None:
            self.fields['oferente'].queryset = Oferente.objects.filter(id_usuario=user)
            
        