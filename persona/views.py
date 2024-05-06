from django.shortcuts import render, redirect
from .forms import RegistroPersonas 
from usuario.views import RegistroUsuario

from django.shortcuts import redirect

def procesar_formulario(request):
    if request.method == 'POST':
        form = RegistroPersonas(request.POST)
        if form.is_valid():
            # Obtener el DNI del formulario
            identificacion = form.cleaned_data['identificacion']  
            # Guardar el formulario de Persona
            form.save()
            # Redirigir a la siguiente vista y pasar el DNI como parámetro en la URL
            return redirect('procesarUsuario', identificacion=identificacion)
    else:
        # Si es una solicitud GET, crear un formulario vacío
        form = RegistroPersonas()
    return render(request, 'registro.html', {'form': form})



def procesarUsuario(request,persona_id):
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
