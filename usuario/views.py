<<<<<<< HEAD
from django.shortcuts import render
from django.views.generic import TemplateView
=======
from django.shortcuts import redirect, render
>>>>>>> parent of 608f4b1 (cambio de contraseña e inicio de sesion)

class Index(TemplateView):
    template_name = 'usuarios/index.html'


<<<<<<< HEAD
=======
def procesarUsuario(request):
    if request.method == 'POST':
        form = RegistroUsuario(request.POST)
        if form.is_valid():
            form.save()
            return redirect('formulario_exitoso')
    else:
        form = RegistroUsuario()
    return render(request, 'registroUsuario.html', {'form': form})
    

def formulario_exitoso(request):
    return render(request, 'formulario_exitoso.html')
>>>>>>> parent of 608f4b1 (cambio de contraseña e inicio de sesion)


# Create your views here.
