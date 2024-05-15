from django import forms
from persona.models import Persona

class FormPersona(forms.ModelForm):

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
                                                     'placeholder': ' Ingrese su DNI (sin puntos)'}),
            'nombres': forms.TextInput(attrs={'class':'block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6',
                                              'placeholder': 'Ingrese su nombre completo'}),
            'apellidos': forms.TextInput(attrs={'class':'block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6',
                                                'placeholder': ' Ingrese su apellido'})
        }
       
       