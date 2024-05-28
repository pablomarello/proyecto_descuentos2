from django import forms
from persona.models import Persona
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV3
from django.forms.utils import ErrorList

class FormPersona(forms.ModelForm):
    # captcha = ReCaptchaField(widget=ReCaptchaV3)

    def __init__(self, *args, **kwargs):
        super(FormPersona, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] += ' mb-2'  # Añadir espacio entre los campos si es necesario
            field.label_tag = lambda label, attrs={}, field_id=None: (
                label and label % field.label or ''
            )
            field.label_attrs = {'class': 'block text-sm font-medium leading-6 text-red-900'}  # Añadir clases personalizadas a los labels

    class Meta:
        model = Persona
        fields = ('identificacion', 'nombres', 'apellidos','foto',)  # Personaliza los campos según tus necesidades
        widgets = {
            'identificacion': forms.TextInput(attrs={'class': 'block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6',
                                                     'placeholder': ' Ingrese su DNI (sin puntos)',
                                                     'min': '1000000',
                                                     'autocomplete': 'off'}),
            'nombres': forms.TextInput(attrs={'class':'block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6',
                                              'placeholder': 'Ingrese su nombre completo','autocomplete': 'off'}),
            'apellidos': forms.TextInput(attrs={'class':'block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6',
                                                'placeholder': ' Ingrese su apellido','autocomplete': 'off'}),
            'foto': forms.FileInput(attrs={'class':'block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 dark:text-gray-400 focus:outline-none dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400',
                                           'id':'inputFile'})
        }
       
    #VALIDACIONES

    #validacion de dni: el valor ingresado no puede ser menor a 1000000
    def clean_identificacion(self):
        identificacion = self.cleaned_data.get('identificacion')
        if identificacion < 1000000:
            raise forms.ValidationError('Debes ingresar un número de DNI superior a 1000000')
        return identificacion
    

       