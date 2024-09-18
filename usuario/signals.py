from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from django.utils import timezone
from .models import ActividadUsuario

@receiver(user_logged_in)
def registrar_inicio_sesion(sender, request, user, **kwargs):
    # Crear un nuevo registro de actividad al iniciar sesión
    actividad = ActividadUsuario.objects.create(usuario=user, actividadinicio=timezone.now())
    actividad.save()

@receiver(user_logged_out)
def registrar_cierre_sesion(sender, request, user, **kwargs):
    try:
        # Actualizar el último registro de actividad con la hora de cierre de sesión
        actividad = ActividadUsuario.objects.filter(usuario=user).latest('actividadinicio')
        actividad.actividadfin = timezone.now()
        actividad.save()
    except ActividadUsuario.DoesNotExist:
        pass
