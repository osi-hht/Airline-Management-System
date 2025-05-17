# from django.db import models

# # ---------------------------
# # AIRPORT
# # ---------------------------
# class Airport(models.Model):
#     name = models.CharField(max_length=100)
#     city = models.CharField(max_length=100)
#     country = models.CharField(max_length=100)

#     def __str__(self):
#         return f"{self.name} ({self.city})"

#     # -- SQL Equivalent --
#     # CREATE TABLE Airport (
#     #   id INTEGER PRIMARY KEY,
#     #   name VARCHAR(100),
#     #   city VARCHAR(100),
#     #   country VARCHAR(100)
#     # );

# # ---------------------------
# # AIRCRAFT
# # ---------------------------
# class Aircraft(models.Model):
#     model = models.CharField(max_length=100)
#     manufacturer = models.CharField(max_length=100)
#     capacity = models.PositiveIntegerField()

#     def __str__(self):
#         return self.model

#     # -- SQL Equivalent --
#     # CREATE TABLE Aircraft (
#     #   id INTEGER PRIMARY KEY,
#     #   model VARCHAR(100),
#     #   manufacturer VARCHAR(100),
#     #   capacity INTEGER
#     # );

# # ---------------------------
# # FLIGHT
# # ---------------------------
# class Flight(models.Model):
#     flight_number = models.CharField(max_length=10, unique=True)
#     source_airport = models.ForeignKey(Airport, related_name="departures", on_delete=models.CASCADE)
#     destination_airport = models.ForeignKey(Airport, related_name="arrivals", on_delete=models.CASCADE)
#     aircraft = models.ForeignKey(Aircraft, on_delete=models.CASCADE)

#     def __str__(self):
#         return self.flight_number

#     # -- SQL Equivalent --
#     # CREATE TABLE Flight (
#     #   id INTEGER PRIMARY KEY,
#     #   flight_number VARCHAR(10) UNIQUE,
#     #   source_airport_id INTEGER REFERENCES Airport(id),
#     #   destination_airport_id INTEGER REFERENCES Airport(id),
#     #   aircraft_id INTEGER REFERENCES Aircraft(id)
#     # );

# # ---------------------------
# # SCHEDULE
# # ---------------------------
# class Schedule(models.Model):
#     flight = models.OneToOneField(Flight, on_delete=models.CASCADE)
#     departure_time = models.DateTimeField()
#     arrival_time = models.DateTimeField()

#     def __str__(self):
#         return f"Schedule for {self.flight}"

#     # -- SQL Equivalent --
#     # CREATE TABLE Schedule (
#     #   id INTEGER PRIMARY KEY,
#     #   flight_id INTEGER UNIQUE REFERENCES Flight(id),
#     #   departure_time TIMESTAMP,
#     #   arrival_time TIMESTAMP
#     # );

# # ---------------------------
# # CREW MEMBER
# # ---------------------------
# class CrewMember(models.Model):
#     name = models.CharField(max_length=100)
#     role = models.CharField(max_length=50)
#     assigned_flight = models.ForeignKey(Flight, on_delete=models.SET_NULL, null=True, blank=True)

#     def __str__(self):
#         return f"{self.name} - {self.role}"

#     # -- SQL Equivalent --
#     # CREATE TABLE CrewMember (
#     #   id INTEGER PRIMARY KEY,
#     #   name VARCHAR(100),
#     #   role VARCHAR(50),
#     #   assigned_flight_id INTEGER NULL REFERENCES Flight(id)
#     # );

# # ---------------------------
# # PASSENGER
# # ---------------------------
# class Passenger(models.Model):
#     first_name = models.CharField(max_length=100)
#     last_name = models.CharField(max_length=100)
#     passport_number = models.CharField(max_length=20, unique=True)
#     nationality = models.CharField(max_length=50)
#     email = models.EmailField()
#     phone = models.CharField(max_length=20)

#     def __str__(self):
#         return f"{self.first_name} {self.last_name}"

#     # -- SQL Equivalent --
#     # CREATE TABLE Passenger (
#     #   id INTEGER PRIMARY KEY,
#     #   first_name VARCHAR(100),
#     #   last_name VARCHAR(100),
#     #   passport_number VARCHAR(20) UNIQUE,
#     #   nationality VARCHAR(50),
#     #   email VARCHAR(254),
#     #   phone VARCHAR(20)
#     # );

# # ---------------------------
# # BOOKING
# # ---------------------------
# class Booking(models.Model):
#     passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE)
#     flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
#     booking_date = models.DateField(auto_now_add=True)
#     seat_number = models.CharField(max_length=5)

#     def __str__(self):
#         return f"Booking {self.id} - {self.passenger}"

#     # -- SQL Equivalent --
#     # CREATE TABLE Booking (
#     #   id INTEGER PRIMARY KEY,
#     #   passenger_id INTEGER REFERENCES Passenger(id),
#     #   flight_id INTEGER REFERENCES Flight(id),
#     #   booking_date DATE,
#     #   seat_number VARCHAR(5)
#     # );

# # ---------------------------
# # PAYMENT
# # ---------------------------
# class Payment(models.Model):
#     booking = models.OneToOneField(Booking, on_delete=models.CASCADE)
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     payment_date = models.DateTimeField(auto_now_add=True)
#     payment_method = models.CharField(max_length=50)

#     def __str__(self):
#         return f"Payment for {self.booking}"

#     # -- SQL Equivalent --
#     # CREATE TABLE Payment (
#     #   id INTEGER PRIMARY KEY,
#     #   booking_id INTEGER UNIQUE REFERENCES Booking(id),
#     #   amount DECIMAL(10,2),
#     #   payment_date TIMESTAMP,
#     #   payment_method VARCHAR(50)
#     # );

# # ---------------------------
# # TICKET
# # ---------------------------
# class Ticket(models.Model):
#     booking = models.OneToOneField(Booking, on_delete=models.CASCADE)
#     ticket_number = models.CharField(max_length=20, unique=True)
#     issued_date = models.DateField(auto_now_add=True)

#     def __str__(self):
#         return self.ticket_number

#     # -- SQL Equivalent --
#     # CREATE TABLE Ticket (
#     #   id INTEGER PRIMARY KEY,
#     #   booking_id INTEGER UNIQUE REFERENCES Booking(id),
#     #   ticket_number VARCHAR(20) UNIQUE,
#     #   issued_date DATE
#     # );

# # ---------------------------
# # BAGGAGE
# # ---------------------------
# class Baggage(models.Model):
#     passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE)
#     weight = models.FloatField()
#     baggage_type = models.CharField(max_length=50)

#     def __str__(self):
#         return f"Baggage {self.id} for {self.passenger}"

#     # -- SQL Equivalent --
#     # CREATE TABLE Baggage (
#     #   id INTEGER PRIMARY KEY,
#     #   passenger_id INTEGER REFERENCES Passenger(id),
#     #   weight FLOAT,
#     #   baggage_type VARCHAR(50)
#     # );

# # ---------------------------
# # BOARDING PASS
# # ---------------------------
# class BoardingPass(models.Model):
#     ticket = models.OneToOneField(Ticket, on_delete=models.CASCADE)
#     gate_number = models.CharField(max_length=5)
#     boarding_time = models.DateTimeField()

#     def __str__(self):
#         return f"Boarding Pass for {self.ticket}"

#     # -- SQL Equivalent --
#     # CREATE TABLE BoardingPass (
#     #   id INTEGER PRIMARY KEY,
#     #   ticket_id INTEGER UNIQUE REFERENCES Ticket(id),
#     #   gate_number VARCHAR(5),
#     #   boarding_time TIMESTAMP
#     # );


from django.db import models

# ---------------------------
# AIRPORT
# ---------------------------
class Airport(models.Model):
    Airport_ID = models.AutoField(primary_key=True)
    Airport_Name = models.CharField(max_length=100, default='Unnamed Airport')
    Location = models.CharField(max_length=100, default='Unknown Location')
    Country = models.CharField(max_length=100, default='Unknown Country')

    def __str__(self):
        return self.Airport_Name


# ---------------------------
# AIRCRAFT
# ---------------------------
class Aircraft(models.Model):
    Aircraft_ID = models.AutoField(primary_key=True)
    Model = models.CharField(max_length=100, default='Generic Model')
    Manufacturer = models.CharField(max_length=100, default='Generic Manufacturer')
    Capacity = models.PositiveIntegerField(default=100)

    def __str__(self):
        return self.Model


# ---------------------------
# FLIGHT
# ---------------------------
class Flight(models.Model):
    Flight_ID = models.AutoField(primary_key=True)
    Flight_Number = models.CharField(max_length=10, unique=True, default='FN000')
    Source_Airport = models.ForeignKey(Airport, related_name='source_flights', on_delete=models.CASCADE, default='Unnamed Airport')
    Destination_Airport = models.ForeignKey(Airport, related_name='destination_flights', on_delete=models.CASCADE, default='Unnamed Airport')
    Aircraft_ID = models.ForeignKey(Aircraft, on_delete=models.CASCADE)
    departure_time = models.DateTimeField(null=True, blank=True)
    arrival_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.Flight_Number


# ---------------------------
# SCHEDULE
# ---------------------------
class Schedule(models.Model):
    Schedule_ID = models.AutoField(primary_key=True)
    Date_Time = models.DateTimeField(null=True, blank=True)
    Flight_ID = models.ForeignKey('Flight', on_delete=models.CASCADE, null=True, blank=True)
    Staff_ID = models.ForeignKey('CrewMember', on_delete=models.CASCADE)

    def __str__(self):
        return f"Schedule {self.Schedule_ID}"


# ---------------------------
# CREW MEMBER
# ---------------------------
class CrewMember(models.Model):
    Crew_ID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=100, default='Unnamed Crew')
    Role = models.CharField(max_length=50, default='Unknown Role')
    Experience = models.PositiveIntegerField(default=1)
    Contact_Information = models.CharField(max_length=100, default='N/A')

    def __str__(self):
        return self.Name


# ---------------------------
# PASSENGER
# ---------------------------
class Passenger(models.Model):
    Passenger_ID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=100, default='Unnamed Passenger')
    Date_of_Birth = models.DateField(null=True, blank=True)
    Phone_Number = models.CharField(max_length=20, null=True, blank=True)
    Address = models.CharField(max_length=200, null=True, blank=True)
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    email = models.EmailField(max_length=254, blank=True, null=True)
    passport_Number = models.CharField(max_length=20, unique=True, blank=True, null=True)

    def __str__(self):
        return self.Name


# ---------------------------
# BOOKING
# ---------------------------
class Booking(models.Model):
    Booking_ID = models.AutoField(primary_key=True)
    Passenger_ID = models.ForeignKey(Passenger, on_delete=models.CASCADE)
    Flight_ID = models.ForeignKey(Flight, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)
    seat_number = models.CharField(max_length=5, blank=True, null=True)

    def __str__(self):
        return f"Booking {self.Booking_ID}"


# ---------------------------
# PAYMENT
# ---------------------------
class Payment(models.Model):
    Payment_ID = models.AutoField(primary_key=True, default = 0)
    Booking_ID = models.ForeignKey(Booking, on_delete=models.CASCADE, null=True, blank=True)
    Amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    Payment_Date = models.DateTimeField(null=True, blank=True)
    PAYMENT_METHOD_CHOICES = [
        ('CC', 'Credit Card'),
        ('DC', 'Debit Card'),
        ('PP', 'PayPal'),
        ('CA', 'Cash'),
        ('OT', 'Other'),
    ]
    Payment_Method = models.CharField(max_length=2, choices=PAYMENT_METHOD_CHOICES, default='OT')

    def __str__(self):
        return f"Payment {self.Payment_ID}"


# ---------------------------
# TICKET
# ---------------------------
class Ticket(models.Model):
    Ticket_ID = models.AutoField(primary_key=True)
    Booking_ID = models.ForeignKey(Booking, on_delete=models.CASCADE)
    Seat_Number = models.CharField(max_length=10, default='N/A')
    Price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    Booking_Status = models.CharField(max_length=50, default='Pending')
    Passenger_ID = models.ForeignKey(Passenger, on_delete=models.CASCADE)
    Flight_ID = models.ForeignKey(Flight, on_delete=models.CASCADE)
    Gate_Number = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return f"Ticket {self.Ticket_ID}"


# ---------------------------
# BAGGAGE
# ---------------------------
class Baggage(models.Model):
    Baggage_ID = models.AutoField(primary_key=True)
    Weight = models.FloatField(default=0.0)
    Type = models.CharField(max_length=50, default='General')
    Passenger_ID = models.ForeignKey(Passenger, on_delete=models.CASCADE)

    def __str__(self):
        return f"Baggage {self.Baggage_ID}"


# ---------------------------
# BOARDING PASS
# ---------------------------
class BoardingPass(models.Model):
    BoardingPass_ID = models.AutoField(primary_key=True)
    Booking_ID = models.ForeignKey(Booking, on_delete=models.CASCADE, null=True, blank=True)
    Seat_Number = models.CharField(max_length=10, null=True, blank=True)
    Flight_ID = models.ForeignKey(Flight, on_delete=models.CASCADE, null=True, blank=True)
    Passenger_ID = models.ForeignKey(Passenger, on_delete=models.CASCADE, null=True, blank=True)
    Barcode = models.CharField(max_length=100, default='TEMP123')
    boarding_time = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Boarding Pass {self.BoardingPass_ID}"
