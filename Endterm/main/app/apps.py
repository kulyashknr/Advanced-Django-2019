from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = 'app'

    def ready(self):
        import app.signals