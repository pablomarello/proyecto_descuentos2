
from django.shortcuts import redirect, render
from django.shortcuts import render,redirect
from django.views.generic import TemplateView
from .forms import LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.auth import get_user_model

from usuario.forms import RegistroUsuario

def login(request):
    if request.method=='POST':
        form= LoginForm(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            user=authenticate(request,username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('index')
                else:
                    messages.error(request, 'Atención: Verifique los Dastos Ingresados')
            else:
                messages.error(request, 'Invalid Login')
    else:
        form = LoginForm()  
    return render(request,'registration/login.html', {'form':form})

def cerrar_sesion(request):
    logout(request)
    return render(request,'base.html')

#cambiar contraseña

class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'registration/password_change_form.html'
    success_url = reverse_lazy('index')

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

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'registration/password_reset_done.html'        

class CustomPasswordResetErrorView(TemplateView):
    template_name = 'registration/password_reset_error.html'    

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'registration/password_reset_confirm.html'

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'registration/password_reset_complete.html'

# Create your views here.
