from importlib import simple
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
import folium.map
from requests import request

from oferta.models import Oferta
from usuario.sms import send_sms
from .forms import LogeoForm
from django.contrib.auth import authenticate,login, logout
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.auth import get_user_model
from django.contrib import messages
from .forms import UsuarioCreationForm
from django.conf import settings
from persona.models import Persona
from django.shortcuts import get_object_or_404
from django.urls import reverse
from .email import *
from .models import *
import random
import folium



def index(request):
    ofertas = Oferta.objects.filter(activo=True)
    
    return render(request, 'usuarios/index.html', {'ofertas':ofertas })

class Index(TemplateView):
    
   template_name='usuarios/index.html'


def mapa(request):
    initial_map=folium.Map(location=[-28.4993802,-65.8233128],zoom_start=5)
    map_html=initial_map._repr_html_()
    context={'map':map_html}
    return render(request, 'usuarios/mapa.html',context)
#Logueo de usuario
#def log(request):
 #   if request.method == 'POST':
  #      username = request.POST['username']
   #     password = request.POST['password']
    #    user = authenticate(request, username=username, password=password)
     #   if user is not None:
      #      login(request, user)
       #     messages.success(request, 'Has iniciado sesión')
        #    return redirect('index')
        #else:
         #   messages.error(request, 'Verifique los datos ingresados')
          #  return redirect('login')
    #else:
     #   return render(request, 'usuarios/login.html')
    
    
#def logout_user(request):
 #   logout(request)
  #  messages.success(request, 'Sesión cerrada')
   # return redirect('logi')





#Creación de usuario y verificacion de email
def generate_verification_token():
    return ''.join([str(random.randint(0, 9)) for _ in range(6)])


def registrar_usuario(request, persona_id):
    persona = get_object_or_404(Persona, pk=persona_id)
    if request.method == 'POST':
        form = UsuarioCreationForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.persona_id = persona

            # Genera token y se guarda en la base de datos
            verification_token = generate_verification_token()
            usuario.token = verification_token
            usuario.save()

            metodo_verificacion = form.cleaned_data['metodo_verificacion']
            email = form.cleaned_data['email']
            telefono = form.cleaned_data['telefono']
            nombreUsuario=usuario.username
            if metodo_verificacion == 'email':
                # Enviar token por email
                send_email_token(email, usuario.token,nombreUsuario)

            elif metodo_verificacion == 'telefono':
                # Enviar token por SMS
                texto = f'Hola {nombreUsuario} - Ingresa el token de seguridad para completar tu registro: {verification_token}-'
                response_text = send_sms(telefono, texto)
                if "ERROR" in response_text:
                    messages.error(request, f'Error al enviar SMS: {response_text}')
                    return render(request, 'usuarios/registro.html', {'form': form})

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
                return redirect('login')
        except Usuario.DoesNotExist:
            messages.error(request, 'Error, verifique los datos igresados')
    return render(request, 'usuarios/verificar_token.html')


class CustomPasswordResetView(PasswordResetView):
    def form_valid(self, form):
        email = form.cleaned_data['email']
        User = get_user_model()
        # Verifica si existe un usuario con el correo electrónico proporcionado
        if User.objects.filter(email=email).exists():
            print('Existe email: '+email)
            # Si existe, envía el correo de restablecimiento de contraseña
            #return super().form_valid(form)
            return super().form_valid(form)
        else:
            # Si no existe, muestra un mensaje de error y redirige a una página de error
            print('No Existe email: '+email)
            #messages.error(self.request, 'No existe una cuenta con este correo electrónico. ' +email)
            #return self.form_invalid(form)
            return redirect('password_reset_error')       
        
#Logueo de usuario

def iniciar_sesion(request):
    if request.method=='POST':
        form= LogeoForm(request.POST)
        if form.is_valid():
            username = request.POST['usuario']
            password = request.POST['contraseña']
            #captcha = request.POST['captcha']
            user=authenticate(request,username=username, password=password)#, captcha=captcha
            if user is not None:
                    login(request, user)
                    return redirect('index')
            else:
                    messages.error(request, 'Verifique los datos ingresados')
                    return redirect('login')
    else:
        form = LogeoForm()  
    return render(request,'registration/login.html', {'form':form})

def cerrar_sesion(request):
    logout(request)
    messages.success(request, 'Sesión cerrada')
    return render(request,'base.html')

#cambiar contraseña

class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'registration/password_change_form.html'
    success_url = reverse_lazy('index')

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'registration/password_reset_done.html'        

class CustomPasswordResetErrorView(TemplateView):
    template_name = 'registration/password_reset_error.html'    

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'registration/password_reset_confirm.html'

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'registration/password_reset_complete.html'


# Create your views here.
