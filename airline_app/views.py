# # # airline_app/views.py
# # from django.shortcuts import render, redirect
# # from django.contrib import messages
# # from django.contrib.auth.decorators import login_required
# # from django.contrib.admin.views.decorators import staff_member_required
# # from django.core.mail import send_mail
# # from django.utils import timezone
# # from datetime import timedelta
# # from .models import Flight, Booking
# # from .forms import FlightSearchForm, BookingForm, FlightForm, UserRegistrationForm
# # from django.http import HttpResponse
# # from django.contrib.auth.models import User
# # from django.contrib.auth import login

# # def home(request):
# #     return render(request, 'base.html')


# # # Flight List View - Show all available flights
# # def flight_list(request):
# #     flights = Flight.objects.all()
# #     return render(request, 'airline_app/flight_list.html', {'flights': flights})

# # # Detailed Flight View
# # def flight_detail(request, flight_id):
# #     flight = Flight.objects.get(id=flight_id)
# #     return render(request, 'airline_app/flight_detail.html', {'flight': flight})

# # # Flight Search View with Advanced Filters
# # def flight_search(request):
# #     if request.method == 'GET':
# #         form = FlightSearchForm(request.GET)
# #         if form.is_valid():
# #             origin = form.cleaned_data['origin']
# #             destination = form.cleaned_data['destination']
# #             departure_date = form.cleaned_data['departure_date']
# #             price_range = form.cleaned_data.get('price_range', None)
# #             airline = form.cleaned_data.get('airline', None)

# #             flights = Flight.objects.all()

# #             if origin:
# #                 flights = flights.filter(origin__icontains=origin)
# #             if destination:
# #                 flights = flights.filter(destination__icontains=destination)
# #             if departure_date:
# #                 flights = flights.filter(departure_date=departure_date)
# #             if price_range:
# #                 flights = flights.filter(price__lte=price_range)
# #             if airline:
# #                 flights = flights.filter(airline__icontains=airline)

# #             return render(request, 'airline_app/flight_list.html', {'flights': flights})
# #         else:
# #             messages.error(request, 'Invalid search criteria. Please correct the errors and try again.')
# #     else:
# #         form = FlightSearchForm()

# #     return render(request, 'airline_app/flight_search.html', {'form': form})

# # # Booking a Flight (User creates a booking or as a Guest)
# # def book_flight(request, flight_id):
# #     flight = Flight.objects.get(id=flight_id)
# #     if request.method == "POST":
# #         form = BookingForm(request.POST)
# #         if form.is_valid():
# #             if request.user.is_authenticated:
# #                 booking = form.save(commit=False)
# #                 booking.user = request.user
# #             else:
# #                 booking = form.save(commit=False)
# #                 booking.user = None

# #             booking.flight = flight
# #             booking.total_amount = flight.price * form.cleaned_data['number_of_seats']
# #             booking.save()

# #             send_mail(
# #                 'Booking Confirmation',
# #                 f"Your booking has been confirmed!\nFlight: {booking.flight.origin} to {booking.flight.destination}\nDate: {booking.flight.departure_date}\nSeats: {booking.number_of_seats}",
# #                 'admin@airline.com',
# #                 [booking.user.email] if booking.user else ['guest@airline.com'],
# #                 fail_silently=False,
# #             )

# #             messages.success(request, 'Booking successful! You can view your booking in your profile or as a guest.')
# #             if request.user.is_authenticated:
# #                 return redirect('user_profile')
# #             else:
# #                 return redirect('guest_booking_history')
# #         else:
# #             messages.error(request, 'There was an issue with your booking. Please check the form and try again.')
# #     else:
# #         form = BookingForm()

# #     return render(request, 'airline_app/book_flight.html', {'form': form, 'flight': flight})

# # # User Profile View (with Booking History)
# # @login_required
# # def user_profile(request):
# #     bookings = Booking.objects.filter(user=request.user)
# #     return render(request, 'airline_app/user_profile.html', {'bookings': bookings})

# # # View Booking History for Guest Users
# # def guest_booking_history(request):
# #     bookings = Booking.objects.filter(user=None)
# #     return render(request, 'airline_app/guest_booking_history.html', {'bookings': bookings})

# # # Modify Booking
# # @login_required
# # def modify_booking(request, booking_id):
# #     booking = Booking.objects.get(id=booking_id)
# #     if booking.user == request.user:
# #         if request.method == 'POST':
# #             form = BookingForm(request.POST, instance=booking)
# #             if form.is_valid():
# #                 form.save()
# #                 messages.success(request, 'Your booking has been modified successfully!')
# #                 return redirect('user_profile')
# #             else:
# #                 messages.error(request, 'There was an issue modifying your booking.')
# #         else:
# #             form = BookingForm(instance=booking)
# #         return render(request, 'airline_app/modify_booking.html', {'form': form, 'booking': booking})
# #     else:
# #         messages.error(request, 'You are not authorized to modify this booking.')
# #         return redirect('user_profile')

# # # Cancel Booking
# # @login_required
# # def cancel_booking(request, booking_id):
# #     booking = Booking.objects.get(id=booking_id)
# #     if booking.user == request.user:
# #         booking.delete()
# #         messages.success(request, 'Your booking has been cancelled.')
# #         return redirect('user_profile')
# #     else:
# #         messages.error(request, 'You are not authorized to cancel this booking.')
# #         return redirect('user_profile')

# # # Dummy Payment Integration (PROTECTED NOW)
# # @login_required
# # def payment_process(request, booking_id):
# #     booking = Booking.objects.get(id=booking_id)

# #     if request.method == 'POST':
# #         booking.payment_status = "Paid"
# #         booking.save()
# #         messages.success(request, 'Payment successful! Your booking is confirmed.')
# #         return redirect('user_profile')

# #     return render(request, 'airline_app/payment_process.html', {'booking': booking})

# # # Admin: Add Flight
# # @staff_member_required
# # def add_flight(request):
# #     if request.method == "POST":
# #         form = FlightForm(request.POST)
# #         if form.is_valid():
# #             form.save()
# #             messages.success(request, 'New flight added successfully!')
# #             return redirect('flight_list')
# #         else:
# #             messages.error(request, 'There was an error adding the flight.')
# #     else:
# #         form = FlightForm()
# #     return render(request, 'airline_app/add_flight.html', {'form': form})

# # # Admin: Edit Flight
# # @staff_member_required
# # def edit_flight(request, flight_id):
# #     flight = Flight.objects.get(id=flight_id)
# #     if request.method == "POST":
# #         form = FlightForm(request.POST, instance=flight)
# #         if form.is_valid():
# #             form.save()
# #             messages.success(request, 'Flight updated successfully!')
# #             return redirect('flight_list')
# #         else:
# #             messages.error(request, 'There was an error updating the flight.')
# #     else:
# #         form = FlightForm(instance=flight)
# #     return render(request, 'airline_app/edit_flight.html', {'form': form, 'flight': flight})

# # # Admin: Delete Flight
# # @staff_member_required
# # def delete_flight(request, flight_id):
# #     flight = Flight.objects.get(id=flight_id)
# #     flight.delete()
# #     messages.success(request, 'Flight deleted successfully!')
# #     return redirect('flight_list')

# # # Admin: View All Bookings
# # @staff_member_required
# # def view_bookings(request):
# #     bookings = Booking.objects.all()
# #     return render(request, 'airline_app/view_bookings.html', {'bookings': bookings})

# # # Admin: View All Flights
# # @staff_member_required
# # def view_flights(request):
# #     flights = Flight.objects.all()
# #     return render(request, 'airline_app/view_flights.html', {'flights': flights})

# # # Admin: Dashboard
# # @staff_member_required
# # def admin_dashboard(request):
# #     total_flights = Flight.objects.count()
# #     total_bookings = Booking.objects.count()
# #     recent_bookings = Booking.objects.order_by('-booking_date')[:5]
# #     return render(request, 'airline_app/admin_dashboard.html', {
# #         'total_flights': total_flights,
# #         'total_bookings': total_bookings,
# #         'recent_bookings': recent_bookings,
# #     })

# # # Admin: Update Booking Status
# # @staff_member_required
# # def update_booking_status(request, booking_id):
# #     booking = Booking.objects.get(id=booking_id)
# #     if request.method == 'POST':
# #         new_status = request.POST.get('status')
# #         if new_status:
# #             booking.status = new_status
# #             booking.save()
# #             messages.success(request, 'Booking status updated successfully.')
# #         return redirect('view_bookings')
# #     return render(request, 'airline_app/update_booking_status.html', {'booking': booking})

# # # Admin: Delete Booking
# # @staff_member_required
# # def delete_booking(request, booking_id):
# #     booking = Booking.objects.get(id=booking_id)
# #     booking.delete()
# #     messages.success(request, 'Booking deleted successfully.')
# #     return redirect('view_bookings')

# # # User Registration View
# # def register(request):
# #     if request.method == 'POST':
# #         form = UserRegistrationForm(request.POST)
# #         if form.is_valid():
# #             user = form.save()
# #             login(request, user)
# #             messages.success(request, 'Registration successful! You are now logged in.')
# #             return redirect('user_profile')
# #         else:
# #             messages.error(request, 'There was an error with your registration. Please check the form and try again.')
# #     else:
# #         form = UserRegistrationForm()
# #     return render(request, 'airline_app/register.html', {'form': form})
# # def about(request):
# #     return render(request, 'about.html')
# # def services(request):
# #     return render(request, 'services.html')
# # def contact(request):
# #     return render(request, 'contact.html')

# # def booking(request):
# #     return render(request, 'booking.html')

# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# from django.contrib.auth.decorators import login_required
# from django.utils import timezone
# from .models import *
# from .forms import PassengerForm, BookingForm
# from django.contrib import messages

# # Home page with flight search form
# def home_view(request):
#     airports = Airport.objects.all()
#     return render(request, 'home.html', {'airports': airports})

# # View for searching flights
# def search_flights_view(request):
#     if request.method == 'POST':
#         source_id = request.POST.get('source')
#         destination_id = request.POST.get('destination')
#         departure_date = request.POST.get('departure_date')

#         flights = Flight.objects.filter(
#             source_id=source_id,
#             destination_id=destination_id,
#             departure__date=departure_date
#         )
#         return render(request, 'search_results.html', {'flights': flights})

#     return redirect('home')

# # View flight details
# def flight_detail_view(request, flight_id):
#     flight = get_object_or_404(Flight, id=flight_id)
#     return render(request, 'flight_detail.html', {'flight': flight})

# # Book a flight (guest or logged-in)
# def book_flight_view(request, flight_id):
#     flight = get_object_or_404(Flight, id=flight_id)

#     if request.method == 'POST':
#         passenger_form = PassengerForm(request.POST)
#         booking_form = BookingForm(request.POST)

#         if passenger_form.is_valid() and booking_form.is_valid():
#             passenger = passenger_form.save()
#             booking = booking_form.save(commit=False)
#             booking.passenger = passenger
#             booking.flight = flight
#             booking.save()

#             # Generate ticket and payment (placeholder)
#             Ticket.objects.create(booking=booking, number=f"T{booking.id}")
#             Payment.objects.create(booking=booking, amount=500.00, method="Cash")

#             messages.success(request, "Flight booked successfully!")
#             return redirect('booking_success', booking.id)

#     else:
#         passenger_form = PassengerForm()
#         booking_form = BookingForm()

#     return render(request, 'book_flight.html', {
#         'flight': flight,
#         'passenger_form': passenger_form,
#         'booking_form': booking_form
#     })

# # Booking confirmation
# def booking_success_view(request, booking_id):
#     booking = get_object_or_404(Booking, id=booking_id)
#     return render(request, 'booking_success.html', {'booking': booking})

# # Signup view
# def signup_view(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             return redirect('home')
#     else:
#         form = UserCreationForm()
#     return render(request, 'signup.html', {'form': form})

# # Login view
# def login_view(request):
#     if request.method == 'POST':
#         form = AuthenticationForm(request, data=request.POST)
#         if form.is_valid():
#             user = form.get_user()
#             login(request, user)
#             return redirect('home')
#     else:
#         form = AuthenticationForm()
#     return render(request, 'login.html', {'form': form})

# # Logout view
# def logout_view(request):
#     logout(request)
#     return redirect('home')

# # View logged-in user's bookings
# @login_required
# def my_bookings_view(request):
#     user_email = request.user.email
#     passengers = Passenger.objects.filter(email=user_email)
#     bookings = Booking.objects.filter(passenger__in=passengers)
#     return render(request, 'my_bookings.html', {'bookings': bookings})

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import SignupForm, LoginForm, FlightSearchForm, BookingForm
from .models import Flight, Passenger, Booking, Ticket, Payment

# Signup view
def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            login(request, user)
            return redirect('home')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

# Login view
def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, "Invalid username or password")
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

# Logout view
def logout_view(request):
    logout(request)
    return redirect('home')

# Home view — show search box for flights (from, to, date)
def home(request):
    form = FlightSearchForm()
    return render(request, 'home.html', {'form': form})

# Search flights view — shows matching flights based on search criteria
def search_flights_view(request):
    form = FlightSearchForm(request.GET or None)
    flights = None
    if form.is_valid():
        source = form.cleaned_data.get('source')
        destination = form.cleaned_data.get('destination')
        departure = form.cleaned_data.get('departure')

        flights = Flight.objects.filter(
            Source_Airport=source,
            Destination_Airport=destination
        )
        if departure:
            flights = flights.filter(departure_time__date=departure)

    return render(request, 'search_results.html', {'form': form, 'flights': flights})

# Flight detail view — show full info of selected flight
def flight_detail(request, flight_id):
    flight = get_object_or_404(Flight, id=flight_id)
    return render(request, 'flight_detail.html', {'flight': flight})

# Book flight view — passenger form + seat select, allow guest or logged-in user
def book_flight(request, flight_id):
    flight = get_object_or_404(Flight, id=flight_id)

    initial_data = {}
    if request.user.is_authenticated:
        try:
            passenger = Passenger.objects.get(user=request.user)
            initial_data = {
                'first_name': passenger.first_name,
                'last_name': passenger.last_name,
                'dob': passenger.dob,
                'gender': passenger.gender,
                'phone': passenger.phone,
                'address': passenger.address,
                'email': passenger.email,
            }
        except Passenger.DoesNotExist:
            pass

    if request.method == 'POST':
        form = BookingForm(request.POST, initial=initial_data)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.flight = flight
            if request.user.is_authenticated:
                try:
                    booking.passenger = Passenger.objects.get(user=request.user)
                except Passenger.DoesNotExist:
                    # For logged in user without passenger profile
                    pass
            booking.save()
            return redirect('confirm_booking_view', booking_id=booking.id)
    else:
        form = BookingForm(initial=initial_data)

    return render(request, 'book_flight.html', {'form': form, 'flight': flight})

# Confirm booking view — booking confirmation + generate ticket, payment
def booking_success(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    # Generate ticket if not exists
    ticket, created = Ticket.objects.get_or_create(booking=booking, defaults={
        'number': f"TICK{booking.id:06d}"
    })

    # Simple payment simulation: in real app handle payment gateway
    if request.method == 'POST':
        amount = request.POST.get('amount')
        method = request.POST.get('method')
        if amount and method:
            payment, created = Payment.objects.get_or_create(booking=booking, defaults={
                'amount': amount,
                'method': method,
            })
            return redirect('booking_success', booking_id=booking.id)

    return render(request, 'confirm_booking.html', {
        'booking': booking,
        'ticket': ticket,
    })

# Show logged-in user's bookings
@login_required
def my_bookings_view(request):
    try:
        passenger = Passenger.objects.get(user=request.user)
        bookings = Booking.objects.filter(passenger=passenger)
    except Passenger.DoesNotExist:
        bookings = []

    return render(request, 'my_bookings.html', {'bookings': bookings})

# Admin panel placeholder (can be extended later)
@login_required
def admin_panel(request):
    if not request.user.is_staff:
        return redirect('home')
    # Later: flight and schedule management
    return render(request, 'admin_panel.html')
