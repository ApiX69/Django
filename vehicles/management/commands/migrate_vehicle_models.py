from django.core.management.base import BaseCommand
from vehicles.models import Vehicle, VehicleModel
from django.db import transaction

class Command(BaseCommand):
    help = 'Migrate existing vehicle model names to VehicleModel entries and update Vehicle records'

    def handle(self, *args, **options):
        with transaction.atomic():
            # Get distinct model names from Vehicle
            model_names = Vehicle.objects.values_list('model', flat=True).distinct()
            self.stdout.write(f"Found {len(model_names)} distinct vehicle model names.")

            # Create VehicleModel entries for each distinct model name
            model_map = {}
            for name in model_names:
                vehicle_model, created = VehicleModel.objects.get_or_create(name=name)
                model_map[name] = vehicle_model
                if created:
                    self.stdout.write(f"Created VehicleModel: {name}")

            # Update Vehicle records to reference VehicleModel
            vehicles = Vehicle.objects.all()
            for vehicle in vehicles:
                model_name = vehicle.model
                vehicle_model = model_map.get(model_name)
                if vehicle_model:
                    vehicle.model = vehicle_model
                    vehicle.save(update_fields=['model'])
                    self.stdout.write(f"Updated Vehicle id={vehicle.id} model to VehicleModel id={vehicle_model.id}")
                else:
                    self.stdout.write(f"Warning: No VehicleModel found for Vehicle id={vehicle.id} model={model_name}")

        self.stdout.write(self.style.SUCCESS('Vehicle model migration completed successfully.'))
