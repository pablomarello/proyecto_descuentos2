from django import forms
from persona.models import Personas

class RegistroPersonas(forms.ModelForm):
    class Meta:
        model = Personas
        fields = ['identificacion','nombres','apellidos','genero','foto']
    
