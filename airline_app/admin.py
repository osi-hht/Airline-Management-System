from django.contrib import admin
from .models import (
    Airport, Aircraft, Flight, Schedule, CrewMember,
    Passenger, Booking, Payment, Ticket, Baggage, BoardingPass
)

admin.site.register(Airport)
admin.site.register(Aircraft)
admin.site.register(Flight)
admin.site.register(Schedule)
admin.site.register(CrewMember)
admin.site.register(Passenger)
admin.site.register(Booking)
admin.site.register(Payment)
admin.site.register(Ticket)
admin.site.register(Baggage)
admin.site.register(BoardingPass)
