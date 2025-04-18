from django.db import models
from django.apps import apps

class Module(models.Model):
    name = models.CharField(max_length=100, unique=True)
    installed = models.BooleanField(default=False)
    version = models.CharField(max_length=20)
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name
    
    @classmethod
    def load_modules(cls):
        """Mendaftarkan semua modul yang tersedia"""
        installed_apps = apps.get_app_configs()
        modules = []
        
        for app in installed_apps:
            if hasattr(app, 'module_config'):
                config = app.module_config
                module, created = cls.objects.get_or_create(
                    name=config['name'],
                    defaults={
                        'version': config['version'],
                        'installed': True
                    }
                )
                if not created:
                    module.version = config['version']
                    module.save()
                modules.append(module)
        
        cls.objects.exclude(name__in=[m.name for m in modules]).update(installed=False)
        
        return modules