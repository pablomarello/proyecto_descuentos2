from django import forms
from django.contrib.auth.forms import AuthenticationForm
from usuario.models import Usuario

class RegistroUsuario(forms.ModelForm):
    class Meta:
        model= Usuario
        fields=['username','clave','email','persona_id']



class LoginForm(forms.ModelForm):
    class Meta:
        model=Usuario
        fields=[]
    

#class FormularioUsuario(forms.ModelForm):
    #Formulario de registro de un usuario en la base de datos
    #definimos las variables extras que queremos agregar al formulario (aparte de las que vienen del modelo indicado en la clase meta)
 #   password1 = forms.CharField(label = 'Contraseña',widget= forms.PasswordInput(
  #      attrs= {
   #         'class': ' form-control',
    #        'placeholder': 'Ingrese su contraseña',
     #       'id': 'password1',
      #      'required': 'required',
       # }
    #))

    #password2 = forms.CharField(label= 'Contraseña de confirmación', widget= forms.PasswordInput(
     #   attrs= {
      #      'class': ' form-control',
       #     'placeholder': 'Ingrese nuevamente su contraseña',
        #    'id': 'password2',
         #   'required': 'required',
        #}
    #))

    class Meta:
        model = Usuario
        #campos que va a utilizar para crearlo: fields = ('__all__') utiliza todos los campos
        #en nuestro caso debemos especificar que campos utilizar (solo los definidos como obligatorios y los que queremos que el usuario realmente vea y cuales no)
        fields = ('email','username','nombres','apellidos')
        widgets = {
            'email': forms.EmailInput(
                attrs= {
                    'class': 'form-control',
                    'placeholder': 'Correo Electrónico',
                }
            ),
            'nombres': forms.TextInput(
                attrs= {
                    'class': 'form-control',
                    'placeholder': 'Ingrese sus nombres',
                }
            ),
            'apellidos': forms.TextInput(
                attrs= {
                    'class': 'form-control',
                    'placeholder': 'Ingrese sus apellidos',
                }
            ),
            'username': forms.TextInput(
                attrs= {
                    'class': 'form-control',
                    'placeholder': 'Ingrese su nombre de usuario',
                }
            )
        }