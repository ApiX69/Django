from django.contrib import admin
from .models import VehicleModel, Vehicle, Mission, Service, TripRequest, FuelCard, TripReport, Driver, ServiceTask

@admin.register(VehicleModel)
class VehicleModelAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('model', 'license_plate', 'status', 'mileage', 'date_bought')

@admin.register(Mission)
class MissionAdmin(admin.ModelAdmin):
    list_display = ('mission_type',)

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(TripRequest)
class TripRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'vehicle', 'mission', 'date_going', 'date_coming_back', 'status')

@admin.register(FuelCard)
class FuelCardAdmin(admin.ModelAdmin):
    list_display = ('balance', 'type')

@admin.register(TripReport)
class TripReportAdmin(admin.ModelAdmin):
    list_display = ('trip_request', 'new_mileage', 'fuel_filled', 'issue_occurred')

@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'cin', 'status', 'date_added')

@admin.register(ServiceTask)
class ServiceTaskAdmin(admin.ModelAdmin):
    list_display = ('vehicle', 'service', 'date_going', 'date_coming_back', 'driver', 'fuel_used')
