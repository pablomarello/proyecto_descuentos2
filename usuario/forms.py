from django import forms
from django.contrib.auth.forms import UserCreationForm
from usuario.models import Usuario
from django.contrib import messages
from django_recaptcha.fields import ReCaptchaField
from django.contrib.auth import authenticate



class UsuarioCreationForm(UserCreationForm):
    captcha=ReCaptchaField()
    class Meta(UserCreationForm.Meta):
        model = Usuario
        fields = ('username', 'password1', 'password2','email')  # Personaliza los campos según tus necesidades
        widgets = {
            'username': forms.TextInput(attrs={'class': "block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6",'autocomplete': 'off'}),
            'password1': forms.PasswordInput(attrs={'class': "block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"}),
            'password2': forms.PasswordInput(attrs={'class': "block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"}),
            'email': forms.EmailInput(attrs={'class': "block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6",'autocomplete': 'off'}),
        }

        def __init__(self, *args, **kwargs):
            super(UsuarioCreationForm, self).__init__(*args, **kwargs)
            for field in self.fields.values():
                field.widget.attrs['class'] += ' mb-2'  # Añadir espacio entre los campos si es necesario
                field.label_tag = lambda label, attrs={}, field_id=None: (
                    label and label % field.label or ''
                )
                field.label_attrs = {'class': 'block text-sm font-medium leading-6 text-red-900'}  # Añadir clases personalizadas a los labels

        def clean_email(self):
            email = self.cleaned_data.get['email']
            if Usuario.objects.filter(email=email).exists():
                raise forms.ValidationError('Este correo electrónico ya está registrado.')
            return email
        
class LogeoForm(forms.Form):
    
    usuario= forms.CharField(max_length=50)
    contraseña= forms.CharField(widget=forms.PasswordInput)
    captcha = ReCaptchaField()

    class Meta():
        model = Usuario
        fields = ('usuario', 'contraseña','captcha')

    #VALIDACIONES

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('usuario')
        password = cleaned_data.get('contraseña')
        captcha = cleaned_data.get('captcha')

        if username and password:
            user = authenticate(username=username, password=password, capctha=captcha)
            if user is None:
                raise forms.ValidationError("El nombre de usuario y/o la contraseña no son correctos")
        return cleaned_data
    
 