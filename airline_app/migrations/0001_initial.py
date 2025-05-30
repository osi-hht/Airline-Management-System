# Generated by Django 5.2 on 2025-05-17 14:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Aircraft',
            fields=[
                ('Aircraft_ID', models.AutoField(primary_key=True, serialize=False)),
                ('Model', models.CharField(default='Generic Model', max_length=100)),
                ('Manufacturer', models.CharField(default='Generic Manufacturer', max_length=100)),
                ('Capacity', models.PositiveIntegerField(default=100)),
            ],
        ),
        migrations.CreateModel(
            name='Airport',
            fields=[
                ('Airport_ID', models.AutoField(primary_key=True, serialize=False)),
                ('Airport_Name', models.CharField(default='Unnamed Airport', max_length=100)),
                ('Location', models.CharField(default='Unknown Location', max_length=100)),
                ('Country', models.CharField(default='Unknown Country', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='CrewMember',
            fields=[
                ('Crew_ID', models.AutoField(primary_key=True, serialize=False)),
                ('Name', models.CharField(default='Unnamed Crew', max_length=100)),
                ('Role', models.CharField(default='Unknown Role', max_length=50)),
                ('Experience', models.PositiveIntegerField(default=1)),
                ('Contact_Information', models.CharField(default='N/A', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Passenger',
            fields=[
                ('Passenger_ID', models.AutoField(primary_key=True, serialize=False)),
                ('Name', models.CharField(default='Unnamed Passenger', max_length=100)),
                ('Date_of_Birth', models.DateField(blank=True, null=True)),
                ('Phone_Number', models.CharField(blank=True, max_length=20, null=True)),
                ('Address', models.CharField(blank=True, max_length=200, null=True)),
                ('gender', models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], max_length=1, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('passport_Number', models.CharField(blank=True, max_length=20, null=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Flight',
            fields=[
                ('Flight_ID', models.AutoField(primary_key=True, serialize=False)),
                ('Flight_Number', models.CharField(default='FN000', max_length=10, unique=True)),
                ('departure_time', models.DateTimeField(blank=True, null=True)),
                ('arrival_time', models.DateTimeField(blank=True, null=True)),
                ('Aircraft_ID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='airline_app.aircraft')),
                ('Destination_Airport', models.ForeignKey(default='Unnamed Airport', on_delete=django.db.models.deletion.CASCADE, related_name='destination_flights', to='airline_app.airport')),
                ('Source_Airport', models.ForeignKey(default='Unnamed Airport', on_delete=django.db.models.deletion.CASCADE, related_name='source_flights', to='airline_app.airport')),
            ],
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('Booking_ID', models.AutoField(primary_key=True, serialize=False)),
                ('booking_date', models.DateTimeField(auto_now_add=True)),
                ('seat_number', models.CharField(blank=True, max_length=5, null=True)),
                ('Flight_ID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='airline_app.flight')),
                ('Passenger_ID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='airline_app.passenger')),
            ],
        ),
        migrations.CreateModel(
            name='BoardingPass',
            fields=[
                ('BoardingPass_ID', models.AutoField(primary_key=True, serialize=False)),
                ('Seat_Number', models.CharField(blank=True, max_length=10, null=True)),
                ('Barcode', models.CharField(default='TEMP123', max_length=100)),
                ('boarding_time', models.DateTimeField(blank=True, null=True)),
                ('Booking_ID', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='airline_app.booking')),
                ('Flight_ID', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='airline_app.flight')),
                ('Passenger_ID', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='airline_app.passenger')),
            ],
        ),
        migrations.CreateModel(
            name='Baggage',
            fields=[
                ('Baggage_ID', models.AutoField(primary_key=True, serialize=False)),
                ('Weight', models.FloatField(default=0.0)),
                ('Type', models.CharField(default='General', max_length=50)),
                ('Passenger_ID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='airline_app.passenger')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('Payment_ID', models.AutoField(default=0, primary_key=True, serialize=False)),
                ('Amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('Payment_Date', models.DateTimeField(blank=True, null=True)),
                ('Payment_Method', models.CharField(choices=[('CC', 'Credit Card'), ('DC', 'Debit Card'), ('PP', 'PayPal'), ('CA', 'Cash'), ('OT', 'Other')], default='OT', max_length=2)),
                ('Booking_ID', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='airline_app.booking')),
            ],
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('Schedule_ID', models.AutoField(primary_key=True, serialize=False)),
                ('Date_Time', models.DateTimeField(blank=True, null=True)),
                ('Flight_ID', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='airline_app.flight')),
                ('Staff_ID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='airline_app.crewmember')),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('Ticket_ID', models.AutoField(primary_key=True, serialize=False)),
                ('Seat_Number', models.CharField(default='N/A', max_length=10)),
                ('Price', models.DecimalField(decimal_places=2, default=0.0, max_digits=8)),
                ('Booking_Status', models.CharField(default='Pending', max_length=50)),
                ('Gate_Number', models.CharField(blank=True, max_length=10, null=True)),
                ('Booking_ID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='airline_app.booking')),
                ('Flight_ID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='airline_app.flight')),
                ('Passenger_ID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='airline_app.passenger')),
            ],
        ),
    ]
