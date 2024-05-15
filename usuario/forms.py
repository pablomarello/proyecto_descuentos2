from django import forms
from django.contrib.auth.forms import UserCreationForm
from usuario.models import Usuario



class UsuarioCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Usuario
        fields = ('username', 'password1', 'password2','email')  # Personaliza los campos según tus necesidades
        widgets = {
            'username': forms.TextInput(attrs={'class': "block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"}),
            'password1': forms.PasswordInput(attrs={'class': "block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"}),
            'password2': forms.PasswordInput(attrs={'class': "block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"}),
            'email': forms.EmailInput(attrs={'class': "block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"}),
        }

        def __init__(self, *args, **kwargs):
            super(UsuarioCreationForm, self).__init__(*args, **kwargs)
            for field in self.fields.values():
                field.widget.attrs['class'] += ' mb-2'  # Añadir espacio entre los campos si es necesario
                field.label_tag = lambda label, attrs={}, field_id=None: (
                    label and label % field.label or ''
                )
                field.label_attrs = {'class': 'block text-sm font-medium leading-6 text-red-900'}  # Añadir clases personalizadas a los labels

        def clean_email(self):
            email = self.cleaned_data['email']
            if Usuario.objects.filter(email=email).exists():
                raise forms.ValidationError('Este correo electrónico ya está registrado.')
            return email
        
""" class FormularioUsuario(forms.ModelForm):
    #Formulario de registro de un usuario en la base de datos
    #definimos las variables extras que queremos agregar al formulario (aparte de las que vienen del modelo indicado en la clase meta)
    password1 = forms.CharField(label = 'Contraseña',widget= forms.PasswordInput(
        attrs= {
            'class': ' form-control',
            'placeholder': 'Ingrese su contraseña',
            'id': 'password1',
            'required': 'required',
        }
    ))

    password2 = forms.CharField(label= 'Contraseña de confirmación', widget= forms.PasswordInput(
        attrs= {
            'class': ' form-control',
            'placeholder': 'Ingrese nuevamente su contraseña',
            'id': 'password2',
            'required': 'required',
        }
    )) """