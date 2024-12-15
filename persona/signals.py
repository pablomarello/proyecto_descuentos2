from .models import Persona
from django.db.models.signals import pre_save
from django.dispatch import receiver

@receiver(pre_save, sender=Persona)
def set_persona_creacion(sender, instance, **kwargs):
    if not instance.pk and hasattr(instance, '_current_user'):
        instance.usuario_creacion = instance._current_user.id