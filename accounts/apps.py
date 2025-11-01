from django.apps import AppConfig

class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'
    
    def ready(self):
        """
        This method is called when the app is ready.
        We don't need to import signals since they're defined in models.py
        """
        pass