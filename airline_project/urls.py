from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('airline_app.urls')),  # replace 'yourappname' with your actual app name
]
