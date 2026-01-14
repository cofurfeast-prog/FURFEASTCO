from django.apps import AppConfig


class FurfeastConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'furfeast'
    
    def ready(self):
        import furfeast.signals
