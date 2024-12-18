from datetime import date
import os
from django import forms

from administracion.models import ConfiguracionSistema
from .models import Comentario, Oferta
from oferente.models import Oferente
from producto.models import Producto

class ComentarioForm(forms.ModelForm):
    class Meta:
        model=Comentario
        fields=['comentario']
        widgets = {'comentario':forms.Textarea(attrs={'class':'form-control','placeholder':'Escribe tu comentario aquí','style': 'border: 1px solid #d1d5db; padding: 4px; border-radius: 4px;'}),}
class OfertaForm(forms.ModelForm):
    
    oferente = forms.ModelChoiceField(
        queryset=Oferente.objects.none(),  # Inicialmente vacío, se llenará en el __init__
        widget=forms.Select,
        required=True,
        label="Oferente"
    )
    imagen = forms.ImageField(
        required=False,  # No obligatorio, el usuario puede no subir una imagen
        widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
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
        # Validación de precios
        precio_normal = cleaned_data.get('precio_normal')
        precio_oferta = cleaned_data.get('precio_oferta')
        if precio_normal is not None and precio_oferta is not None:
            # Comprobar que precio_normal es estrictamente mayor que precio_oferta
            if precio_normal <= precio_oferta:
                self.add_error('precio_normal', "El precio normal debe ser mayor al precio de la oferta.")
        
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
    
       
    def clean_imagen(self):
        imagen = self.cleaned_data.get('imagen')

        # Verifica si se ha subido una imagen
        if imagen:
            	

            # Obtiene la extensión del archivo
            extension = os.path.splitext(imagen.name)[1][1:].lower()  # Obtiene la extensión sin el punto

            # Obtiene los formatos permitidos desde la configuración del sistema
            configuracion = ConfiguracionSistema.objects.first()
            if configuracion and configuracion.formatos_imagen_permitidos:
                formatos_permitidos = configuracion.formatos_imagen_permitidos.split(",")
            else:
                formatos_permitidos = ['jpg', 'png', 'gif', 'bmp', 'webp']  # Valores predeterminados

            # Verifica si la extensión está en los formatos permitidos
            if extension not in formatos_permitidos:
                raise forms.ValidationError(
                    f"El formato de la imagen no es válido. Los formatos permitidos son: {', '.join(formatos_permitidos)}"
                )
        return imagen

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Obtener el usuario del argumento kwargs
        super().__init__(*args, **kwargs)

        # Filtrar los comercios asociados al usuario
        if user is not None:
            self.fields['oferente'].queryset = Oferente.objects.filter(id_usuario=user)


        