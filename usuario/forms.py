from django import forms
from django.contrib.auth.forms import AuthenticationForm
from usuario.models import Usuario

class RegistroUsuario(forms.ModelForm):
    class Meta:
        model= Usuario
        fields=['username','clave','email','persona_id']



class FormularioUsuario(forms.ModelForm):
    #Formulario de registro de un usuario en la base de datos
    #definimos las variables extras que queremos agregar al formulario (aparte de las que vienen del modelo indicado en la clase meta)
    password1 = forms.CharField(label = 'Contraseña',widget= forms.PasswordInput(
        attrs= {
            'class': ' form-control',
            'placeholder': 'Ingrese su contraseña',
            'id': 'password1',
            'required': 'required',
        }
    ))

    password2 = forms.CharField(label= 'Contraseña de confirmación', widget= forms.PasswordInput(
        attrs= {
            'class': ' form-control',
            'placeholder': 'Ingrese nuevamente su contraseña',
            'id': 'password2',
            'required': 'required',
        }
    ))

    