from django import forms
from .models import Producto, Categoria, Subcategoria

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'imagen', 'marca', 'categoria']
        widgets = {
            'descripcion': forms.Textarea(attrs={'maxlength': '300'}),  # Limitar a 300 caracteres visualmente
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar subcategorías activas
        self.fields['categoria'].queryset = Subcategoria.objects.filter(eliminado=False)

    #Validaciones

    def clean_descripcion(self):
        descripcion = self.cleaned_data.get('descripcion')
        if len(descripcion) > 300:
            raise forms.ValidationError("La descripción no puede superar los 300 caracteres.")
        return descripcion
    
    def clean_marca(self):
        marca = self.cleaned_data.get('marca')
        if len(marca) > 100:
            raise forms.ValidationError("La marca no puede superar los 100 caracteres.")
        return marca
    
    def clean_categoria(self):
        categoria = self.cleaned_data.get('categoria')
        if not categoria:
            raise forms.ValidationError("Debe asignar una categoría para el producto.")
        return categoria
