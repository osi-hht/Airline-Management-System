from django import forms
from .models import Flight, Booking, Passenger, Schedule
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.utils import timezone

# ---------------------------
# USER REGISTRATION FORM
# ---------------------------
class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

# ---------------------------
# FLIGHT SEARCH FORM
# ---------------------------
class FlightSearchForm(forms.Form):
    origin = forms.CharField(required=False, max_length=100, label='Origin')
    destination = forms.CharField(required=False, max_length=100, label='Destination')
    departure_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}), label='Departure Date')
    airline = forms.CharField(required=False, max_length=100, label='Airline')

    def clean_departure_date(self):
        date = self.cleaned_data.get('departure_date')
        if date and date < timezone.now().date():
            raise ValidationError("Departure date must be today or in the future.")
        return date

# ---------------------------
# PASSENGER FORM (Used with Booking)
# ---------------------------
class PassengerForm(forms.ModelForm):
    class Meta:
        model = Passenger
        fields = ['first_name', 'last_name', 'passport_number', 'nationality', 'email', 'phone']

# ---------------------------
# BOOKING FORM
# ---------------------------
class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['flight', 'seat_number']

    def clean_seat_number(self):
        seat = self.cleaned_data.get('seat_number')
        if not seat:
            raise ValidationError("Seat number is required.")
        return seat

# ---------------------------
# FLIGHT CREATION / UPDATE FORM (ADMIN)
# ---------------------------
class FlightForm(forms.ModelForm):
    class Meta:
        model = Flight
        fields = ['flight_number', 'source_airport', 'destination_airport', 'aircraft']

# ---------------------------
# SCHEDULE FORM (ADMIN)
# ---------------------------
class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ['flight', 'departure_time', 'arrival_time']
        widgets = {
            'departure_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'arrival_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        departure = cleaned_data.get("departure_time")
        arrival = cleaned_data.get("arrival_time")

        if departure and arrival and departure >= arrival:
            raise ValidationError("Arrival time must be after departure time.")

# ---------------------------
# BOOKING UPDATE FORM (ADMIN)
# ---------------------------
class BookingUpdateForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['flight', 'seat_number']

# ---------------------------
# FLIGHT DELETE FORM (ADMIN)
# ---------------------------
class FlightDeleteForm(forms.Form):
    flight_id = forms.IntegerField(widget=forms.HiddenInput())

    def clean_flight_id(self):
        from .models import Flight
        fid = self.cleaned_data['flight_id']
        if not Flight.objects.filter(id=fid).exists():
            raise ValidationError("Flight does not exist.")
        return fid

# ---------------------------
# BOOKING DELETE FORM (ADMIN)
# ---------------------------
class BookingDeleteForm(forms.Form):
    booking_id = forms.IntegerField(widget=forms.HiddenInput())

    def clean_booking_id(self):
        from .models import Booking
        bid = self.cleaned_data['booking_id']
        if not Booking.objects.filter(id=bid).exists():
            raise ValidationError("Booking does not exist.")
        return bid
