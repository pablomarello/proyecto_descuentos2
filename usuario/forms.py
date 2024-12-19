from django import forms
from django.contrib.auth.forms import UserCreationForm
from usuario.models import Usuario
from django.contrib import messages
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.fields import ReCaptchaField
from django.contrib.auth import authenticate
from proyecto_descuentos2.settings import RECAPTCHA_PUBLIC_KEY, RECAPTCHA_PRIVATE_KEY
from django.contrib.auth.forms import PasswordResetForm


"""    captcha  =  ReCaptchaField ( 
        public_key =RECAPTCHA_PUBLIC_KEY, 
        private_key = RECAPTCHA_PRIVATE_KEY,
    )
    """
    


class UsuarioCreationForm(UserCreationForm):
    ENVIO_CHOICES = [
        ('email', 'Email'),
        ('telefono', 'Teléfono'),
    ]
    
    metodo_verificacion = forms.ChoiceField( choices=ENVIO_CHOICES,widget=forms.RadioSelect, label="Prefiero recibir el token por", initial='email')#
    telefono = forms.IntegerField(required=False, label="Número de Teléfono", widget=forms.TextInput(attrs={
        'class': "w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-red-400 focus:border-red-400",
        'autocomplete': 'off',
        'type':'number',
        'placeholder':'Ingrese su número de teléfono'
    }))
    email = forms.CharField(required=False, label="Correo electrónico", max_length=40, widget=forms.TextInput(attrs={
        'class': "w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-red-400 focus:border-red-400",
        'autocomplete': 'off',
        'placeholder':'Ingrese su correo electrónico'
    }))

    class Meta(UserCreationForm.Meta):
        model = Usuario
        fields = ('username', 'password1', 'password2', 'email', 'metodo_verificacion', 'telefono')  # Incluye los nuevos campos

    def __init__(self, *args, **kwargs):
        super(UsuarioCreationForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = field.widget.attrs.get('class', '') + ' mb-2'
            field.label_tag = lambda label, attrs={}, field_id=None: (label and label % field.label or '')
            field.label_attrs = {'class': 'block text-sm font-medium leading-6 text-red-900'}

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and Usuario.objects.filter(email=email).exists():
            raise forms.ValidationError('Este correo electrónico ya está registrado.')
        return email

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if telefono and Usuario.objects.filter(telefono=telefono).exists():
            raise forms.ValidationError('Este número de teléfono ya está registrado.')
        return telefono

    def clean(self):
        cleaned_data = super().clean()
        metodo_verificacion = cleaned_data.get('metodo_verificacion')
        telefono = cleaned_data.get('telefono')
        if metodo_verificacion == 'telefono' and not telefono:
            self.add_error('telefono', 'El número de teléfono es requerido si selecciona recibir el token por Teléfono.')
        return cleaned_data
    
    

class LogeoForm(forms.Form):
    
    usuario= forms.CharField(max_length=50, widget=forms.TextInput(attrs={'autocomplete': 'off',
    'class':"w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-red-400 focus:border-red-400"})
    )
    contraseña= forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete': 'off',
    'class':'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-red-400 focus:border-red-400'}))
    captcha  =  ReCaptchaField ( 
        label='',
        public_key =RECAPTCHA_PUBLIC_KEY, 
        private_key = RECAPTCHA_PRIVATE_KEY,
    )

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
    