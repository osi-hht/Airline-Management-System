# project/urls.py (main project URL configuration)
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('airline/', include('airline_app.urls')),  # Include airline app's URLs
]
