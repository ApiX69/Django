from django.db import models
from django.conf import settings

class VehicleModel(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Vehicle(models.Model):
    STATUS_CHOICES = [
        ('free', 'Free'),
        ('in_use', 'In Use'),
    ]

    model = models.ForeignKey(VehicleModel, on_delete=models.CASCADE)
    year = models.PositiveIntegerField()
    license_plate = models.CharField(max_length=20, unique=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='free')
    horsepower = models.PositiveIntegerField(null=True, blank=True)
    fuel_type = models.ForeignKey('FuelType', on_delete=models.SET_NULL, null=True, blank=True)
    mileage = models.PositiveIntegerField(null=True, blank=True)
    date_bought = models.DateField(null=True, blank=True)
    # Removed mission_type field as per request
    # mission_type = models.ForeignKey('Mission', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f" {self.model} ({self.license_plate})"

class Mission(models.Model):
    mission_type = models.CharField(max_length=100)

    def __str__(self):
        return self.mission_type

class Service(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class TripRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('in_trip', 'In Trip'),
        ('reported', 'Reported'),
        ('trip_ended', 'Trip Ended'),
        ('rejected', 'Rejected'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True, blank=True)
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE)
    date_going = models.DateField()
    date_coming_back = models.DateField()
    motif = models.TextField()
    destination = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    fuel_used = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"TripRequest by {self.user} for {self.vehicle} ({self.status})"

class Driver(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    cin = models.CharField(max_length=20, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.cin})"

class FuelType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.name

class TripReport(models.Model):
    trip_request = models.OneToOneField('TripRequest', on_delete=models.CASCADE, related_name='report')
    report_text = models.TextField()
    old_mileage = models.PositiveIntegerField(null=True, blank=True)
    new_mileage = models.PositiveIntegerField()
    fuel_filled = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    issue_occurred = models.BooleanField(default=False)
    issue_detail = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Report for {self.trip_request}"

class ServiceTask(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True, blank=True)
    date_going = models.DateField()
    date_coming_back = models.DateField()
    destination = models.CharField(max_length=255)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    fuel_used = models.DecimalField(max_digits=6, decimal_places=2)
    motif = models.TextField()

    def __str__(self):
        return f"ServiceTask for {self.vehicle} with {self.driver} ({self.date_going} to {self.date_coming_back})"
