from django.urls import path
from . import views

urlpatterns = [
    path('', views.module_manager, name='module_manager'),    
     path('upgrade/<str:module_name>/', views.module_upgrade_form, name='module_upgrade_form'),
]