from django.core.management.base import BaseCommand
from django.utils import timezone
from vehicles.models import Vehicle, MissionOrder

class Command(BaseCommand):
    help = 'Update trip request and vehicle statuses based on current date'

    def handle(self, *args, **options):
        today = timezone.now().date()

        # Update trip requests to in_trip if current date is between date_going and date_coming_back
        in_trip_requests = MissionOrder.objects.filter(
            status='approved',
            date_going__lte=today,
            date_coming_back__gte=today
        )
        for trip in in_trip_requests:
            trip.status = 'in_trip'
            trip.save()
            vehicle = trip.vehicle
            if vehicle and vehicle.status != 'in_use':
                vehicle.status = 'in_use'
                vehicle.save()
            self.stdout.write(f"MissionOrder {trip.pk} set to in_trip; Vehicle {vehicle} set to in_use.")

        # Update trip requests to trip_ended if current date is after date_coming_back
        ended_trips = MissionOrder.objects.filter(
            status__in=['approved', 'in_trip'],
            date_coming_back__lt=today
        )
        for trip in ended_trips:
            trip.status = 'trip_ended'
            trip.save()
            vehicle = trip.vehicle
            # Check if vehicle has any other ongoing trips
            ongoing_trips = MissionOrder.objects.filter(
                vehicle=vehicle,
                status__in=['approved', 'in_trip'],
                date_coming_back__gte=today
            )
            if not ongoing_trips.exists():
                vehicle.status = 'free'
                vehicle.save()
            self.stdout.write(f"MissionOrder {trip.pk} set to trip_ended; Vehicle {vehicle} set to free.")
