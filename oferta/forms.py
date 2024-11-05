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
        