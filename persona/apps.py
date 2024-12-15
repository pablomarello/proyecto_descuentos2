from django.apps import AppConfig


class PersonaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'persona'

    def ready(self):
        import persona.signals
