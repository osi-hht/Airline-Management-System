from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin URL here
    path('', views.home, name='home'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('search/', views.search_flights_view, name='search_flights_view'),  # Added this line
    path('flight/<int:flight_id>/', views.flight_detail, name='flight_detail'),
    path('flight/<int:flight_id>/book/', views.book_flight, name='book_flight'),
    path('booking/success/<int:booking_id>/', views.booking_success, name='booking_success'),
]