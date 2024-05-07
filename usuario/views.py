from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth import authenticate,login, logout
from django.contrib import messages
from .forms import UsuarioCreationForm
from django.shortcuts import render
from django.views.generic import TemplateView
from django.shortcuts import redirect, render

class Index(TemplateView):
    template_name = 'usuarios/index.html'

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Bienvenido')
            return redirect('index')
        else:
            messages.success(request, 'Algo salió mal')
            return redirect('login')
    else:
        return render(request, 'usuarios/login.html')

def registrar(request):
    if request.method == 'POST':
        form = UsuarioCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            email = form.cleaned_data['email']
            user = authenticate(username=username, password=password, email=email)
            login(request, user)
            messages.success(request, 'Registo completado con exito')
            return redirect('registrar_persona')
    else:
        form = UsuarioCreationForm()
    return render(request, 'usuarios/registro.html', {'form': form})

def logout_user(request):
    logout(request)
    messages.success(request, 'Sesión cerrada')
    return redirect('login_user')




# Create your views here.
