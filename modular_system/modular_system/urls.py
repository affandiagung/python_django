from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("module/", include("module_engine.urls")),
    path("", include("example_module.urls")),
]
