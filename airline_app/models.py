from django.db import models

# ---------------------------
# AIRPORT
# ---------------------------
class Airport(models.Model):
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.city})"

    # -- SQL Equivalent --
    # CREATE TABLE Airport (
    #   id INTEGER PRIMARY KEY,
    #   name VARCHAR(100),
    #   city VARCHAR(100),
    #   country VARCHAR(100)
    # );

# ---------------------------
# AIRCRAFT
# ---------------------------
class Aircraft(models.Model):
    model = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=100)
    capacity = models.PositiveIntegerField()

    def __str__(self):
        return self.model

    # -- SQL Equivalent --
    # CREATE TABLE Aircraft (
    #   id INTEGER PRIMARY KEY,
    #   model VARCHAR(100),
    #   manufacturer VARCHAR(100),
    #   capacity INTEGER
    # );

# ---------------------------
# FLIGHT
# ---------------------------
class Flight(models.Model):
    flight_number = models.CharField(max_length=10, unique=True)
    source_airport = models.ForeignKey(Airport, related_name="departures", on_delete=models.CASCADE)
    destination_airport = models.ForeignKey(Airport, related_name="arrivals", on_delete=models.CASCADE)
    aircraft = models.ForeignKey(Aircraft, on_delete=models.CASCADE)

    def __str__(self):
        return self.flight_number

    # -- SQL Equivalent --
    # CREATE TABLE Flight (
    #   id INTEGER PRIMARY KEY,
    #   flight_number VARCHAR(10) UNIQUE,
    #   source_airport_id INTEGER REFERENCES Airport(id),
    #   destination_airport_id INTEGER REFERENCES Airport(id),
    #   aircraft_id INTEGER REFERENCES Aircraft(id)
    # );

# ---------------------------
# SCHEDULE
# ---------------------------
class Schedule(models.Model):
    flight = models.OneToOneField(Flight, on_delete=models.CASCADE)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()

    def __str__(self):
        return f"Schedule for {self.flight}"

    # -- SQL Equivalent --
    # CREATE TABLE Schedule (
    #   id INTEGER PRIMARY KEY,
    #   flight_id INTEGER UNIQUE REFERENCES Flight(id),
    #   departure_time TIMESTAMP,
    #   arrival_time TIMESTAMP
    # );

# ---------------------------
# CREW MEMBER
# ---------------------------
class CrewMember(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=50)
    assigned_flight = models.ForeignKey(Flight, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.role}"

    # -- SQL Equivalent --
    # CREATE TABLE CrewMember (
    #   id INTEGER PRIMARY KEY,
    #   name VARCHAR(100),
    #   role VARCHAR(50),
    #   assigned_flight_id INTEGER NULL REFERENCES Flight(id)
    # );

# ---------------------------
# PASSENGER
# ---------------------------
class Passenger(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    passport_number = models.CharField(max_length=20, unique=True)
    nationality = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    # -- SQL Equivalent --
    # CREATE TABLE Passenger (
    #   id INTEGER PRIMARY KEY,
    #   first_name VARCHAR(100),
    #   last_name VARCHAR(100),
    #   passport_number VARCHAR(20) UNIQUE,
    #   nationality VARCHAR(50),
    #   email VARCHAR(254),
    #   phone VARCHAR(20)
    # );

# ---------------------------
# BOOKING
# ---------------------------
class Booking(models.Model):
    passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE)
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    booking_date = models.DateField(auto_now_add=True)
    seat_number = models.CharField(max_length=5)

    def __str__(self):
        return f"Booking {self.id} - {self.passenger}"

    # -- SQL Equivalent --
    # CREATE TABLE Booking (
    #   id INTEGER PRIMARY KEY,
    #   passenger_id INTEGER REFERENCES Passenger(id),
    #   flight_id INTEGER REFERENCES Flight(id),
    #   booking_date DATE,
    #   seat_number VARCHAR(5)
    # );

# ---------------------------
# PAYMENT
# ---------------------------
class Payment(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=50)

    def __str__(self):
        return f"Payment for {self.booking}"

    # -- SQL Equivalent --
    # CREATE TABLE Payment (
    #   id INTEGER PRIMARY KEY,
    #   booking_id INTEGER UNIQUE REFERENCES Booking(id),
    #   amount DECIMAL(10,2),
    #   payment_date TIMESTAMP,
    #   payment_method VARCHAR(50)
    # );

# ---------------------------
# TICKET
# ---------------------------
class Ticket(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)
    ticket_number = models.CharField(max_length=20, unique=True)
    issued_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.ticket_number

    # -- SQL Equivalent --
    # CREATE TABLE Ticket (
    #   id INTEGER PRIMARY KEY,
    #   booking_id INTEGER UNIQUE REFERENCES Booking(id),
    #   ticket_number VARCHAR(20) UNIQUE,
    #   issued_date DATE
    # );

# ---------------------------
# BAGGAGE
# ---------------------------
class Baggage(models.Model):
    passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE)
    weight = models.FloatField()
    baggage_type = models.CharField(max_length=50)

    def __str__(self):
        return f"Baggage {self.id} for {self.passenger}"

    # -- SQL Equivalent --
    # CREATE TABLE Baggage (
    #   id INTEGER PRIMARY KEY,
    #   passenger_id INTEGER REFERENCES Passenger(id),
    #   weight FLOAT,
    #   baggage_type VARCHAR(50)
    # );

# ---------------------------
# BOARDING PASS
# ---------------------------
class BoardingPass(models.Model):
    ticket = models.OneToOneField(Ticket, on_delete=models.CASCADE)
    gate_number = models.CharField(max_length=5)
    boarding_time = models.DateTimeField()

    def __str__(self):
        return f"Boarding Pass for {self.ticket}"

    # -- SQL Equivalent --
    # CREATE TABLE BoardingPass (
    #   id INTEGER PRIMARY KEY,
    #   ticket_id INTEGER UNIQUE REFERENCES Ticket(id),
    #   gate_number VARCHAR(5),
    #   boarding_time TIMESTAMP
    # );


