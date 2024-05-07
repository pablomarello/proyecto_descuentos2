from django import forms
from persona.models import Persona

class FormPersona(forms.ModelForm):
    class Meta:
        model = Persona
        fields = ('identificacion', 'nombres', 'apellidos')  # Personaliza los campos según tus necesidades
        