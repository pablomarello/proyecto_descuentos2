from django import forms
from oferente.models import Oferente, ubicacionesComercio
from django_recaptcha.fields import ReCaptchaField
from persona.models import TablaDepartamento, TablaLocalidad, TablaMunicipio, TablaPais, TablaProvincia
from proyecto_descuentos2.settings import RECAPTCHA_PUBLIC_KEY, RECAPTCHA_PRIVATE_KEY


""" label='CUIT',
        max_length=11,
        min_length=11,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingresa el CUIT',
            'autocomplete': 'off',
            'pattern': '[0-9]{11}',  
            'maxlength': '11',
            'title': 'Debe ser un número de 11 dígitos',
            'style': 'border: 1px solid #d1d5db; padding-left: 10px; border-radius: 4px;'
        })) """

class CuitForm(forms.Form):
    
    cuit = forms.CharField(
        label='CUIT', 
        max_length=11, 
        min_length=11,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-red-400 focus:border-red-400',       # Clases de Bootstrap o Tailwind para estilos
            'placeholder': 'Ingresa el CUIT',
            'autocomplete': 'off',         # Evita el autocompletado
            'pattern': '[0-9]{11}',        # Asegura que solo se permitan 11 dígitos
            'title': 'Debe ser un número de 11 dígitos',
            'style': 'border: 1px solid #d1d5db; padding: 2px; border-radius: 4px;'
        })
    )
        
    
    
    captcha  =  ReCaptchaField ( 
        label='',
        public_key =RECAPTCHA_PUBLIC_KEY, 
        private_key = RECAPTCHA_PRIVATE_KEY,
    )
    
    def clean_cuit(self):
        cuit = self.cleaned_data.get('cuit')
        if not cuit.isdigit():
            raise forms.ValidationError("El CUIT debe contener solo números.")
        return cuit
    
    
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
        fields = ('nombrecomercio', 'categoria',) # Personaliza los campos según tus necesidades
        labels = {
            'nombrecomercio': 'Nombre del Comercio',  # Nuevo label personalizado
            'categoria': 'Categoría del Comercio',   # Nuevo label personalizado
        }
        widgets = {
            'nombrecomercio': forms.TextInput(attrs={
                'class': "form-control w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-red-400 focus:border-red-500",
                'placeholder': 'Ingrese el nombre del comercio',
                'autocomplete': 'off'
            }),
            
            'categoria': forms.TextInput(attrs={
                'class': 'form-control w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-red-400 focus:border-red-500',
                'placeholder': 'Ingrese la categoría para su comercio',
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
    
    
class UbiComercio(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UbiComercio, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.label_suffix = ""
            
            if isinstance(field.widget, forms.Select):
                field.widget.attrs.update({'class': 'mt-1 p-2 block w-full border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-red-400 focus:border-red-400 select2'})
            else:
                field.widget.attrs.update({'class': 'mt-1 p-2 block w-full border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-red-400 focus:border-red-400'})
        
        # Cargar dinámicamente las provincias, departamentos, etc.
        if 'pais' in self.data:
            try:
                pais_id = int(self.data.get('pais'))
                self.fields['provincia'].queryset = TablaProvincia.objects.filter(pais_id_id=pais_id).order_by('nom_pcia')
            except (ValueError, TypeError):
                self.fields['provincia'].queryset = TablaProvincia.objects.none()

        if 'provincia' in self.data:
            try:
                provincia_id = int(self.data.get('provincia'))
                self.fields['departamento'].queryset = TablaDepartamento.objects.filter(provincia_id_id=provincia_id).order_by('nom_depto')
            except (ValueError, TypeError):
                self.fields['departamento'].queryset = TablaDepartamento.objects.none()

        if 'departamento' in self.data:
            try:
                departamento_id = int(self.data.get('departamento'))
                self.fields['municipio'].queryset = TablaMunicipio.objects.filter(departamento_id_id=departamento_id).order_by('nom_agl')
            except (ValueError, TypeError):
                self.fields['municipio'].queryset = TablaMunicipio.objects.none()

        if 'municipio' in self.data:
            try:
                municipio_id = int(self.data.get('municipio'))
                self.fields['localidad'].queryset = TablaLocalidad.objects.filter(municipio_id_id=municipio_id).order_by('nombre')
            except (ValueError, TypeError):
                self.fields['localidad'].queryset = TablaLocalidad.objects.none()
       
       
       
    class Meta:
        model = ubicacionesComercio
        fields = [
            'pais', 'provincia', 'departamento', 'municipio', 'localidad',
            'barrio', 'calle', 'altura','latitud','longitud'
        ]
        widgets = {
            'pais': forms.Select(attrs={'class': 'form-control select2'}),
            'provincia': forms.Select(attrs={'class': 'block w-full rounded-md border-gray-300 shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'}),
            'departamento': forms.Select(attrs={'class': 'form-control select2'}),
            'municipio': forms.Select(attrs={'class': 'form-control select2'}),
            'localidad': forms.Select(attrs={'class': 'form-control select2'}),
            'barrio': forms.TextInput(attrs={'class':'block w-full rounded-md border-gray-300 shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                                              'placeholder': 'Ingrese el barrio','autocomplete': 'off'}),
            'calle': forms.TextInput(attrs={'class':'block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6',
                                                'placeholder': 'Ingrese la calle','autocomplete': 'off'}),
            'altura': forms.TextInput(attrs={'class':'block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6',
                                              'placeholder': 'Ingrese la altura','autocomplete': 'off'}),
            'latitud': forms.HiddenInput(),
            'longitud': forms.HiddenInput(),
        }
           
            # Agrega más widgets si es necesario
        

    pais = forms.ModelChoiceField(queryset=TablaPais.objects.all(), widget=forms.Select(attrs={'class': 'form-control select2'}))
    provincia = forms.ModelChoiceField(queryset=TablaProvincia.objects.none(), widget=forms.Select(attrs={'class': 'form-control select2'}))
    departamento = forms.ModelChoiceField(queryset=TablaDepartamento.objects.none(), widget=forms.Select(attrs={'class': 'form-control select2'}))
    municipio = forms.ModelChoiceField(queryset=TablaMunicipio.objects.none(), widget=forms.Select(attrs={'class': 'form-control select2'}))
    localidad = forms.ModelChoiceField(queryset=TablaLocalidad.objects.none(), widget=forms.Select(attrs={'class': 'form-control select2'}))
    
