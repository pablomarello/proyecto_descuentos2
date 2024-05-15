from django.shortcuts import render, redirect
from .forms import FormPersona
# Create your views here.
def registrar_persona(request):
    if request.method == 'POST':
        form = FormPersona(request.POST)
        if form.is_valid():
            persona = form.save() # Guarda la instancia de Persona creada con los datos del formulario
             # Redirige al formulario de registro de usuario pasando el ID de la persona creada como parámetro
            print(persona.pk)
            return redirect('registrar_usuario', persona_id=persona.pk)
    else:
        form = FormPersona()
    return render(request, 'personas/registro_personas.html', {'form': form})