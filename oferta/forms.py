from datetime import date
from django import forms
from .models import Comentario, Oferta
from oferente.models import Oferente
from producto.models import Producto

class OfertaForm(forms.ModelForm):
    
    oferente = forms.ModelChoiceField(
        queryset=Oferente.objects.none(),  # Inicialmente vacío, se llenará en el __init__
        widget=forms.Select,
        required=True,
        label="Oferente"
    )

    class Meta:
        model = Oferta
        fields = ['titulo', 'descripcion', 'precio_normal', 'precio_oferta', 'oferente', 'fecha_inicio', 'fecha_fin', 'imagen']
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date'}),
            'fecha_fin': forms.DateInput(attrs={'type': 'date'}),
            
        }
    
    def clean(self):
        cleaned_data = super().clean()
        fecha_inicio = cleaned_data.get("fecha_inicio")
        fecha_fin = cleaned_data.get("fecha_fin")

        # Verificá que ambas fechas estén presentes
        if fecha_inicio and fecha_fin:
            # Comprobá que la fecha de inicio sea anterior o igual a la de fin
            if fecha_inicio > fecha_fin:
                raise forms.ValidationError("La fecha de inicio no puede ser posterior a la fecha de fin.")
            # Comprobá que la fecha de inicio sea hoy o en el futuro
            if fecha_inicio < date.today():
                raise forms.ValidationError("La fecha de inicio debe ser hoy o una fecha futura.")

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Obtener el usuario del argumento kwargs
        super().__init__(*args, **kwargs)

        # Filtrar los comercios asociados al usuario
        if user is not None:
            self.fields['oferente'].queryset = Oferente.objects.filter(id_usuario=user)

class ComentarioForm(forms.ModelForm):
    class Meta:
        model=Comentario
        fields=['comentario']
        widgets = {'comentario':forms.Textarea(attrs={'class':'form-control','placeholder':'Escribe tu comentario aquí','style': 'border: 1px solid #d1d5db; padding: 4px; border-radius: 4px;'}),}
        