from django.shortcuts import redirect, render

from usuario.forms import RegistroUsuario


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


# Create your views here.
