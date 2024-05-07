from django.shortcuts import render, redirect
from .forms import FormPersona
# Create your views here.
def registrar_persona(request):
    if request.method == 'POST':
        form = FormPersona(request.POST)
        if form.is_valid():
            usu = form.save(commit=False) #no se guarda el formulario aun
            usu.usuario_id = request.user #se le asigna el usuario que esta logeado(autenticado antes en el registro de usuario)
            usu.save()
            return redirect('index')
    else:
        form = FormPersona()
    return render(request, 'personas/registro_personas.html', {'form': form})