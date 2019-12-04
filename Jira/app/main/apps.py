from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = 'main'

    def ready(self):
        import main.signals
