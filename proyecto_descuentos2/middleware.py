from django.shortcuts import redirect
from django.urls import reverse

class RedirectUnauthenticatedMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Ruta del login de administradores
        admin_login_path = reverse('login_superuser')  # Asegúrate de que el nombre coincida con el de tu URL

        # Si el usuario no está autenticado y no está accediendo al login de administradores
        if (
            not request.user.is_authenticated
            and not request.user.is_staff
            and not request.user.is_superuser
            and request.path.startswith('/administracion/')
            and request.path != admin_login_path  # Excluir la ruta del login
        ):
            return redirect('login_superuser')  # Redirigir al login para administradores
        
        return self.get_response(request)
