from django.apps import AppConfig

class ExampleModuleConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'example_module'
    
    module_config = {
        'name': 'example_module',
        'version': '1.0.0',
        'description': 'Contoh Module dengan Product Management'
    }
    
    def ready(self):
        if not hasattr(self, 'already_loaded'):
            from . import signals 
            self.already_loaded = True