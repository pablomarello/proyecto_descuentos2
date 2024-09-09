from django import forms
from oferente.models import Oferente
from django_recaptcha.fields import ReCaptchaField
from proyecto_descuentos2.settings import RECAPTCHA_PUBLIC_KEY, RECAPTCHA_PRIVATE_KEY


class CuitForm(forms.Form):
    
    cuit = forms.CharField(label='CUIT', max_length=11, min_length=11)
    captcha  =  ReCaptchaField ( 
        public_key =RECAPTCHA_PUBLIC_KEY, 
        private_key = RECAPTCHA_PRIVATE_KEY,
    )
class OferenteForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(OferenteForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = True
            field.widget.attrs['class'] = field.widget.attrs.get('class', '') + ' mb-2'  # Añadir espacio entre los campos si es necesario
            field.label_tag = lambda label, attrs={}, field_id=None: (
                label and label % field.label or ''
            )
            field.label_attrs = {'class': 'block text-sm font-medium leading-6 text-red-900'}  # Añadir clases personalizadas a los labels

    class Meta:
        model = Oferente
        fields = ('nombrecomercio', 'direccion',) # Personaliza los campos según tus necesidades
        widgets = {
            'nombrecomercio': forms.TextInput(attrs={
                'class': "block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6",
                'placeholder': 'Ingrese NOMBRE DE COMERCIO',
                'autocomplete': 'off'
            }),
            
            'direccion': forms.TextInput(attrs={
                'class': 'block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6',
                'placeholder': 'Ingrese su DIRECCION',
                'autocomplete': 'off'
            }),
           
        }

    # VALIDACIONES
def clean_nombreComercio(self):
        nombrecomercio = self.cleaned_data.get('nombrecomercio')
        if nombrecomercio and Oferente.objects.filter(nombrecomercio=nombrecomercio).exists():
            raise forms.ValidationError('Este nombre de comercio ya existe.')
        return nombrecomercio
    
def clean_cuit(self):
        cuit = self.cleaned_data.get('cuit')
        if cuit and Oferente.objects.filter(cuit=cuit).exists():
            raise forms.ValidationError('Este cuit ya está registrado.')
        return cuit