from django import forms
from django.contrib.auth.forms import UserCreationForm
from usuario.models import Usuario


class UsuarioCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Usuario
        fields = ('username', 'password1', 'password2','email')  # Personaliza los campos según tus necesidades

        def clean_email(self):
            email = self.cleaned_data['email']
            if Usuario.objects.filter(email=email).exists():
                raise forms.ValidationError('Este correo electrónico ya está registrado.')
            return email
        
""" class FormularioUsuario(forms.ModelForm):
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
    )) """