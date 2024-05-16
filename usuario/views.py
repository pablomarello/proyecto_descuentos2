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
from django.urls import reverse
from .email import *
from .models import *
import random




class Index(TemplateView):
    template_name = 'usuarios/index.html'

#Logueo de usuario
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
            messages.error(request, 'Verifique los datos ingresados')
            return redirect('login_user')
    else:
        return render(request, 'usuarios/login.html')
    
    
def logout_user(request):
    logout(request)
    messages.success(request, 'Sesión cerrada')
    return redirect('login_user')





#Creación de usuario y verificacion de email
def generate_verification_token():
    return ''.join([str(random.randint(0, 9)) for _ in range(6)])


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

            #Genera token y se guarda en la base de datos
            verification_token = generate_verification_token()
            usuario.token=verification_token
            usuario.save()

            #enviamos el email y redireccionamos a la vista token_input
            send_email_token(email,usuario.token)
            return redirect(reverse('token_input'))
        else:
            messages.error(request, 'Verifique los datos que está ingresando')
    else:
        
        form = UsuarioCreationForm()
    return render(request, 'usuarios/registro.html', {'form': form})



#Verifica el token
def token_input(request):
    if request.method == 'POST':
        token = request.POST.get('token')
        try:
            profile = Usuario.objects.get(token=token)
            if profile.token == token:
                profile.is_active = True
                profile.save()
                messages.success(request, 'Tu email ha sido verificado exitosamente')
                return redirect('login_user')
        except Usuario.DoesNotExist:
            messages.error(request, 'Error, verifique los datos igresados')
    return render(request, 'usuarios/verificar_token.html')





# Create your views here.
