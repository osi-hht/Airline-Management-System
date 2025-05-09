# airline_app/management/commands/import_airports.py

import requests
from django.core.management.base import BaseCommand
from airline_app.models import Airport

class Command(BaseCommand):
    help = 'Import airports from API Ninjas (Pakistan only)'

    def handle(self, *args, **kwargs):
        url = "https://api.api-ninjas.com/v1/airports?country=PK"
        headers = {
            "X-Api-Key": "ArHY04JUurZAH0m96PFlYg==mcDmyUgLmLrswLru"
        }

        print("Fetching airport data from API...")
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            for item in data:
                airport, created = Airport.objects.get_or_create(
                    name=item.get("name", "Unknown"),
                    city=item.get("city", "Unknown"),
                    country=item.get("country", "Unknown")
                )
                if created:
                    print(f"✔ Added: {airport.name} - {airport.city}, {airport.country}")
                else:
                    print(f"➖ Already exists: {airport.name}")
        else:
            print(f"❌ Failed to fetch data. Status Code: {response.status_code}")
