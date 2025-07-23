from django.apps import AppConfig


class NannyPetsAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'nanny_pets_app'

    def ready(self):
        import nanny_pets_app.signals  # importa os signals ao iniciar o app
