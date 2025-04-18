from django.db import models
from django.contrib.auth.models import Group

class Product(models.Model):
    name = models.CharField(max_length=100)
    barcode = models.CharField(max_length=50, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    @classmethod
    def check_permission(cls, user, action):
        """Cek permission berdasarkan role"""
        if user.is_superuser:
            return True
            
        if action == 'view':
            return True
            
        if not user.is_authenticated:
            return False
            
        if action in ['add', 'change'] and user.groups.filter(name__in=['user', 'manager']).exists():
            return True

        if action == 'delete' and user.groups.filter(name='manager').exists():
            return True
            
        return False