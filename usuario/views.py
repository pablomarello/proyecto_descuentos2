from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth import authenticate,login, logout
from django.contrib import messages
from .forms import UsuarioCreationForm
from django.shortcuts import render
from django.views.generic import TemplateView
from django.shortcuts import redirect, render
from persona.models import Persona
from django.shortcuts import get_object_or_404


class Index(TemplateView):
    template_name = 'usuarios/index.html'

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Has iniciado sesión')
            return redirect('index')
        else:
            messages.error(request, 'Datos incorrectos')
            return redirect('login_user')
    else:
        return render(request, 'usuarios/login.html')

def registrar_usuario(request, persona_id):
    persona = get_object_or_404(Persona, pk=persona_id)
    if request.method == 'POST':
        """ persona_id = request.POST.get('identificacion')
        persona = Persona.objects.get(identificacion=persona_id) """  # Obtiene la instancia de Persona utilizando el ID pasado como parámetro
        form = UsuarioCreationForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            email = form.cleaned_data['email']
            # Asigna la persona al usuario como una clave foránea
            usuario.persona_id = persona
            usuario.save()
            login(request, usuario)
            messages.success(request, 'Registo completado con exito')
            return redirect('index')
        else:
            messages.error(request, 'Verifique los datos que está ingresando')
    else:
        
        form = UsuarioCreationForm()
    return render(request, 'usuarios/registro.html', {'form': form})

def logout_user(request):
    logout(request)
    messages.success(request, 'Sesión cerrada')
    return redirect('login_user')




# Create your views here.
