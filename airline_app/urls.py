# airline_app/urls.py
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('flights/', views.flight_list, name='flight_list'),
    path('flight/<int:flight_id>/', views.flight_detail, name='flight_detail'),
    path('flight/search/', views.flight_search, name='flight_search'),
    path('book/<int:flight_id>/', views.book_flight, name='book_flight'),
    path('profile/', views.user_profile, name='user_profile'),
    path('guest-bookings/', views.guest_booking_history, name='guest_booking_history'),
    path('modify-booking/<int:booking_id>/', views.modify_booking, name='modify_booking'),
    path('cancel-booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('payment/<int:booking_id>/', views.payment_process, name='payment_process'),

    # Admin URLs
    path('admin/add-flight/', views.add_flight, name='add_flight'),
    path('admin/edit-flight/<int:flight_id>/', views.edit_flight, name='edit_flight'),
    path('admin/delete-flight/<int:flight_id>/', views.delete_flight, name='delete_flight'),
    path('admin/view-bookings/', views.view_bookings, name='view_bookings'),
    path('admin/view-flights/', views.view_flights, name='view_flights'),

    # Authentication URLs
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', views.register, name='register'),
]
