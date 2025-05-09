# airline_app/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from .models import Flight, Booking
from .forms import FlightSearchForm, BookingForm, FlightForm, UserRegistrationForm
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login

# Home Page View
def home(request):
    return render(request, 'airline_app/home.html')

# Flight List View - Show all available flights
def flight_list(request):
    flights = Flight.objects.all()
    return render(request, 'airline_app/flight_list.html', {'flights': flights})

# Detailed Flight View
def flight_detail(request, flight_id):
    flight = Flight.objects.get(id=flight_id)
    return render(request, 'airline_app/flight_detail.html', {'flight': flight})

# Flight Search View with Advanced Filters
def flight_search(request):
    if request.method == 'GET':
        form = FlightSearchForm(request.GET)
        if form.is_valid():
            origin = form.cleaned_data['origin']
            destination = form.cleaned_data['destination']
            departure_date = form.cleaned_data['departure_date']
            price_range = form.cleaned_data.get('price_range', None)
            airline = form.cleaned_data.get('airline', None)

            flights = Flight.objects.all()

            if origin:
                flights = flights.filter(origin__icontains=origin)
            if destination:
                flights = flights.filter(destination__icontains=destination)
            if departure_date:
                flights = flights.filter(departure_date=departure_date)
            if price_range:
                flights = flights.filter(price__lte=price_range)
            if airline:
                flights = flights.filter(airline__icontains=airline)

            return render(request, 'airline_app/flight_list.html', {'flights': flights})
        else:
            messages.error(request, 'Invalid search criteria. Please correct the errors and try again.')
    else:
        form = FlightSearchForm()

    return render(request, 'airline_app/flight_search.html', {'form': form})

# Booking a Flight (User creates a booking or as a Guest)
def book_flight(request, flight_id):
    flight = Flight.objects.get(id=flight_id)
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            if request.user.is_authenticated:
                booking = form.save(commit=False)
                booking.user = request.user
            else:
                booking = form.save(commit=False)
                booking.user = None

            booking.flight = flight
            booking.total_amount = flight.price * form.cleaned_data['number_of_seats']
            booking.save()

            send_mail(
                'Booking Confirmation',
                f"Your booking has been confirmed!\nFlight: {booking.flight.origin} to {booking.flight.destination}\nDate: {booking.flight.departure_date}\nSeats: {booking.number_of_seats}",
                'admin@airline.com',
                [booking.user.email] if booking.user else ['guest@airline.com'],
                fail_silently=False,
            )

            messages.success(request, 'Booking successful! You can view your booking in your profile or as a guest.')
            if request.user.is_authenticated:
                return redirect('user_profile')
            else:
                return redirect('guest_booking_history')
        else:
            messages.error(request, 'There was an issue with your booking. Please check the form and try again.')
    else:
        form = BookingForm()

    return render(request, 'airline_app/book_flight.html', {'form': form, 'flight': flight})

# User Profile View (with Booking History)
@login_required
def user_profile(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'airline_app/user_profile.html', {'bookings': bookings})

# View Booking History for Guest Users
def guest_booking_history(request):
    bookings = Booking.objects.filter(user=None)
    return render(request, 'airline_app/guest_booking_history.html', {'bookings': bookings})

# Modify Booking
@login_required
def modify_booking(request, booking_id):
    booking = Booking.objects.get(id=booking_id)
    if booking.user == request.user:
        if request.method == 'POST':
            form = BookingForm(request.POST, instance=booking)
            if form.is_valid():
                form.save()
                messages.success(request, 'Your booking has been modified successfully!')
                return redirect('user_profile')
            else:
                messages.error(request, 'There was an issue modifying your booking.')
        else:
            form = BookingForm(instance=booking)
        return render(request, 'airline_app/modify_booking.html', {'form': form, 'booking': booking})
    else:
        messages.error(request, 'You are not authorized to modify this booking.')
        return redirect('user_profile')

# Cancel Booking
@login_required
def cancel_booking(request, booking_id):
    booking = Booking.objects.get(id=booking_id)
    if booking.user == request.user:
        booking.delete()
        messages.success(request, 'Your booking has been cancelled.')
        return redirect('user_profile')
    else:
        messages.error(request, 'You are not authorized to cancel this booking.')
        return redirect('user_profile')

# Dummy Payment Integration (PROTECTED NOW)
@login_required
def payment_process(request, booking_id):
    booking = Booking.objects.get(id=booking_id)

    if request.method == 'POST':
        booking.payment_status = "Paid"
        booking.save()
        messages.success(request, 'Payment successful! Your booking is confirmed.')
        return redirect('user_profile')

    return render(request, 'airline_app/payment_process.html', {'booking': booking})

# Admin: Add Flight
@staff_member_required
def add_flight(request):
    if request.method == "POST":
        form = FlightForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'New flight added successfully!')
            return redirect('flight_list')
        else:
            messages.error(request, 'There was an error adding the flight.')
    else:
        form = FlightForm()
    return render(request, 'airline_app/add_flight.html', {'form': form})

# Admin: Edit Flight
@staff_member_required
def edit_flight(request, flight_id):
    flight = Flight.objects.get(id=flight_id)
    if request.method == "POST":
        form = FlightForm(request.POST, instance=flight)
        if form.is_valid():
            form.save()
            messages.success(request, 'Flight updated successfully!')
            return redirect('flight_list')
        else:
            messages.error(request, 'There was an error updating the flight.')
    else:
        form = FlightForm(instance=flight)
    return render(request, 'airline_app/edit_flight.html', {'form': form, 'flight': flight})

# Admin: Delete Flight
@staff_member_required
def delete_flight(request, flight_id):
    flight = Flight.objects.get(id=flight_id)
    flight.delete()
    messages.success(request, 'Flight deleted successfully!')
    return redirect('flight_list')

# Admin: View All Bookings
@staff_member_required
def view_bookings(request):
    bookings = Booking.objects.all()
    return render(request, 'airline_app/view_bookings.html', {'bookings': bookings})

# Admin: View All Flights
@staff_member_required
def view_flights(request):
    flights = Flight.objects.all()
    return render(request, 'airline_app/view_flights.html', {'flights': flights})

# Admin: Dashboard
@staff_member_required
def admin_dashboard(request):
    total_flights = Flight.objects.count()
    total_bookings = Booking.objects.count()
    recent_bookings = Booking.objects.order_by('-booking_date')[:5]
    return render(request, 'airline_app/admin_dashboard.html', {
        'total_flights': total_flights,
        'total_bookings': total_bookings,
        'recent_bookings': recent_bookings,
    })

# Admin: Update Booking Status
@staff_member_required
def update_booking_status(request, booking_id):
    booking = Booking.objects.get(id=booking_id)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status:
            booking.status = new_status
            booking.save()
            messages.success(request, 'Booking status updated successfully.')
        return redirect('view_bookings')
    return render(request, 'airline_app/update_booking_status.html', {'booking': booking})

# Admin: Delete Booking
@staff_member_required
def delete_booking(request, booking_id):
    booking = Booking.objects.get(id=booking_id)
    booking.delete()
    messages.success(request, 'Booking deleted successfully.')
    return redirect('view_bookings')

# User Registration View
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful! You are now logged in.')
            return redirect('user_profile')
        else:
            messages.error(request, 'There was an error with your registration. Please check the form and try again.')
    else:
        form = UserRegistrationForm()
    return render(request, 'airline_app/register.html', {'form': form})
