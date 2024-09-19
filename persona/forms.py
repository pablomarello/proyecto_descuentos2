from tkinter.tix import Form, Select
from django import forms
from persona.models import Persona
from persona.models import ubicaciones,TablaPais,TablaProvincia,TablaDepartamento,TablaMunicipio,TablaLocalidad
from  django_recaptcha.fields  import  ReCaptchaField
from  django_recaptcha.widgets  import  ReCaptchaV2Invisible
from django.core.exceptions import ValidationError
from django.forms.utils import ErrorList
from django_select2 import forms as s2forms
from proyecto_descuentos2.settings import RECAPTCHA_PUBLIC_KEY, RECAPTCHA_PRIVATE_KEY



class FormPersona(forms.ModelForm):
    captcha  =  ReCaptchaField ( 
        public_key =RECAPTCHA_PUBLIC_KEY, 
        private_key = RECAPTCHA_PRIVATE_KEY,
    )
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
        fields = ('identificacion', 'nombres', 'apellidos')  # Personaliza los campos según tus necesidades
        widgets = {
            'identificacion': forms.TextInput(attrs={'class': "block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6",
                                                     'placeholder': ' Ingrese su DNI (sin puntos)',
                                                     'min': '1000000',
                                                     'autocomplete': 'off'}),
            'nombres': forms.TextInput(attrs={'class':'block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6',
                                              'placeholder': 'Ingrese su nombre completo','autocomplete': 'off'}),
            'apellidos': forms.TextInput(attrs={'class':'block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6',
                                                'placeholder': ' Ingrese su apellido','autocomplete': 'off'})
        }
    
    #VALIDACIONES

    #validacion de contraseña: el valor ingresado no puede ser menor a 1000000
    def clean_identificacion(self):
        identificacion = self.cleaned_data.get('identificacion')
        if identificacion < 1000000:
            raise forms.ValidationError('Debes ingresar un número de DNI superior a 1000000')
        return identificacion
    
    

#class PaisWidget(s2forms.ModelSelect2Widget):
 #   search_fields={
  #      "nom_pais__icontains"
   # }

#class ProvWidget(s2forms.ModelSelect2Widget):
#    search_fields={
 #       'nom_pcia__icontains'
  #  }
#class DeptpWidget(s2forms.ModelSelect2Widget):
 #   search_fields={
  #      'nom_depto__icontains'
   # }

#class LocalidadWidget(s2forms.ModelSelect2Widget):
 #   search_fields={
  #      'nombre__icontains'
   # }

#class MuniWiget(s2forms.ModelSelect2Widget):
 #   search_fields={
  #      'nom_agl__icontains'
   # }
    
#class FormUbicacion(forms.ModelForm):
 #   def __init__(self, *args, **kwargs):
  #      super(FormUbicacion, self).__init__(*args, **kwargs)
   #     for field in self.fields.values():
            #field.widget.attrs['class'] += ' mb-2'  # Añadir espacio entre los campos si es necesario
    #        field.label_tag = lambda label, attrs={}, field_id=None: (
     #           label and label % field.label or ''
      #      )
       #     field.label_attrs = {'class': 'block text-sm font-medium leading-6 text-red-900'} 
    #class Meta:
     #   model=ubicaciones
      #  fields={
       #     'pais',
        #    'provincia',
         #   'departamento',
          #  'municipio',
           # 'localidad',
            #'barrio',
            #'calle',
            #'altura'
        #}
        #widgets={
         #   'pais': PaisWidget,
          #  'provincia': ProvWidget,
           # 'departamento': DeptpWidget,
            #'municipio': MuniWiget,
            #'localidad':LocalidadWidget, 
        #}        


class Formubi(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(Formubi, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.label_suffix = ""
            
            if isinstance(field.widget, forms.Select):
                field.widget.attrs.update({'class': 'form-control select2'})
            else:
                field.widget.attrs.update({'class': 'form-control'})
        
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
        model = ubicaciones
        fields = [
            'pais', 'provincia', 'departamento', 'municipio', 'localidad',
            'barrio', 'calle', 'altura','latitud','longitud'
        ]
        widgets = {
            'pais': forms.Select(attrs={'class': 'form-control select2'}),
            'provincia': forms.Select(attrs={'class': 'form-control select2'}),
            'departamento': forms.Select(attrs={'class': 'form-control select2'}),
            'municipio': forms.Select(attrs={'class': 'form-control select2'}),
            'localidad': forms.Select(attrs={'class': 'form-control select2'}),
            'barrio': forms.TextInput(attrs={'class':'block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6',
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
    
