from datetime import date
from django import forms
from oferta.models import Oferta
from usuario.models import Usuario
from oferente.models import Oferente
from persona.models import Persona
from django import forms
from django.contrib.auth import authenticate

from django.contrib.auth import authenticate
from django import forms

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

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        user = authenticate(username=username, password=password)

        if user is None:
            raise forms.ValidationError("Nombre de usuario o contraseña incorrectos.")

        if not user.is_superuser:
            raise forms.ValidationError("No tienes permisos para acceder al panel.")

        self.cleaned_data['user'] = user  # Aquí asignamos el usuario autenticado
        return self.cleaned_data



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
        fields = ['username', 'email', 'is_active','persona']
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
            
        