# from django import forms
# from .models import Flight, Booking, Passenger, Schedule
# from django.core.exceptions import ValidationError
# from django.contrib.auth.models import User
# from django.utils import timezone

# # ---------------------------
# # USER REGISTRATION FORM
# # ---------------------------
# class UserRegistrationForm(forms.ModelForm):
#     password1 = forms.CharField(widget=forms.PasswordInput)
#     password2 = forms.CharField(widget=forms.PasswordInput)

#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password1', 'password2']

#     def clean(self):
#         cleaned_data = super().clean()
#         p1 = cleaned_data.get("password1")
#         p2 = cleaned_data.get("password2")
#         if p1 != p2:
#             raise ValidationError("Passwords do not match")
#         return cleaned_data

#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.set_password(self.cleaned_data["password1"])
#         if commit:
#             user.save()
#         return user


# # ---------------------------
# # FLIGHT SEARCH FORM
# # ---------------------------
# class FlightSearchForm(forms.Form):
#     origin = forms.CharField(required=False, max_length=100, label='Origin')
#     destination = forms.CharField(required=False, max_length=100, label='Destination')
#     departure_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}), label='Departure Date')
#     airline = forms.CharField(required=False, max_length=100, label='Airline')

#     def clean_departure_date(self):
#         date = self.cleaned_data.get('departure_date')
#         if date and date < timezone.now().date():
#             raise ValidationError("Departure date must be today or in the future.")
#         return date

# # ---------------------------
# # PASSENGER FORM (Used with Booking)
# # ---------------------------
# class PassengerForm(forms.ModelForm):
#     class Meta:
#         model = Passenger
#         fields = ['first_name', 'last_name', 'passport_number', 'nationality', 'email', 'phone']

# # ---------------------------
# # BOOKING FORM
# # ---------------------------
# class BookingForm(forms.ModelForm):
#     number_of_seats = forms.IntegerField(min_value=1)

#     class Meta:
#         model = Booking
#         fields = ['flight', 'seat_number', 'number_of_seats']


# # ---------------------------
# # FLIGHT CREATION / UPDATE FORM (ADMIN)
# # ---------------------------
# class FlightForm(forms.ModelForm):
#     class Meta:
#         model = Flight
#         fields = ['flight_number', 'source_airport', 'destination_airport', 'aircraft']

# # ---------------------------
# # SCHEDULE FORM (ADMIN)
# # ---------------------------
# class ScheduleForm(forms.ModelForm):
#     class Meta:
#         model = Schedule
#         fields = ['flight', 'departure_time', 'arrival_time']
#         widgets = {
#             'departure_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
#             'arrival_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
#         }

#     def clean(self):
#         cleaned_data = super().clean()
#         departure = cleaned_data.get("departure_time")
#         arrival = cleaned_data.get("arrival_time")

#         if departure and arrival and departure >= arrival:
#             raise ValidationError("Arrival time must be after departure time.")

# # ---------------------------
# # BOOKING UPDATE FORM (ADMIN)
# # ---------------------------
# class BookingUpdateForm(forms.ModelForm):
#     class Meta:
#         model = Booking
#         fields = ['flight', 'seat_number']

# # ---------------------------
# # FLIGHT DELETE FORM (ADMIN)
# # ---------------------------
# class FlightDeleteForm(forms.Form):
#     flight_id = forms.IntegerField(widget=forms.HiddenInput())

#     def clean_flight_id(self):
#         from .models import Flight
#         fid = self.cleaned_data['flight_id']
#         if not Flight.objects.filter(id=fid).exists():
#             raise ValidationError("Flight does not exist.")
#         return fid

# # ---------------------------
# # BOOKING DELETE FORM (ADMIN)
# # ---------------------------
# class BookingDeleteForm(forms.Form):
#     booking_id = forms.IntegerField(widget=forms.HiddenInput())

#     def clean_booking_id(self):
#         from .models import Booking
#         bid = self.cleaned_data['booking_id']
#         if not Booking.objects.filter(id=bid).exists():
#             raise ValidationError("Booking does not exist.")
#         return bid
from django import forms
from .models import Passenger, Booking, Airport
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import date

class PassengerForm(forms.ModelForm):
    class Meta:
        model = Passenger
        fields = [
            'Name', 'Date_of_Birth', 'gender',
            'Phone_Number', 'Address', 'email', 'passport_Number'
        ]
        widgets = {
            'Date_of_Birth': forms.DateInput(attrs={'type': 'date'}),
            'gender': forms.Select(),
            'Phone_Number': forms.TextInput(attrs={'placeholder': 'e.g. +123456789'}),
            'Address': forms.Textarea(attrs={'rows': 2}),
            'email': forms.EmailInput(attrs={'placeholder': 'example@email.com'}),
        }

    def clean_Date_of_Birth(self):
        dob = self.cleaned_data.get('Date_of_Birth')
        if dob >= date.today():
            raise forms.ValidationError("Date of birth cannot be today or in the future.")
        return dob

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['seat_number']
        widgets = {
            'seat_number': forms.TextInput(attrs={
                'placeholder': 'Enter seat number, e.g. 12A',
                'class': 'form-control',
            }),
        }

    def clean_seat_number(self):
        seat = self.cleaned_data.get('seat_number')
        if not seat:
            raise forms.ValidationError("Seat number is required.")
        return seat

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'placeholder': 'Username'}),
        label="Username"
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),
        label="Password"
    )

class FlightSearchForm(forms.Form):
    source = forms.ModelChoiceField(
        queryset=Airport.objects.all(),
        label="From",
        empty_label="Select departure airport"
    )
    destination = forms.ModelChoiceField(
        queryset=Airport.objects.all(),
        label="To",
        empty_label="Select arrival airport"
    )
    departure = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Departure Date (optional)"
    )

class SignupForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),
        label="Password"
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}),
        label="Confirm Password"
    )

    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise ValidationError("Passwords do not match.")

        return cleaned_data
