from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from django.contrib import messages
from .models import Vehicle, VehicleModel, Mission, MissionOrder, FuelCard, TripReport, Driver, ServiceOrder, Service, Department

from .forms import VehicleForm, VehicleModelForm, MissionForm, TripRequestForm, FuelCardForm, TripReportForm, DriverForm, ServiceOrderForm, ServiceForm, DepartmentForm, MissionOrderManagerForm

@login_required
@user_passes_test(lambda u: u.is_authenticated and u.role == 'manager')
def department_list_view(request):
    departments = Department.objects.all()
    return render(request, 'vehicles/department_list.html', {'departments': departments})

@login_required
@user_passes_test(lambda u: u.is_authenticated and u.role == 'manager')
def department_create_view(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('department_list')
    else:
        form = DepartmentForm()
    return render(request, 'vehicles/department_form.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.is_authenticated and u.role == 'manager')
def department_update_view(request, pk):
    department = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            return redirect('department_list')
    else:
        form = DepartmentForm(instance=department)
    return render(request, 'vehicles/department_form.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.is_authenticated and u.role == 'manager')
def department_delete_view(request, pk):
    department = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        department.delete()
        return redirect('department_list')
    return render(request, 'vehicles/department_confirm_delete.html', {'department': department})

@login_required
@user_passes_test(lambda u: u.is_authenticated and u.role == 'manager')
def fuel_card_list_view(request):
    fuel_cards = FuelCard.objects.all()
    return render(request, 'vehicles/fuel_card_list.html', {'fuel_cards': fuel_cards})

@login_required
@user_passes_test(lambda u: u.is_authenticated and u.role == 'manager')
def fuel_card_create_view(request):
    if request.method == 'POST':
        form = FuelCardForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('fuel_card_list')
    else:
        form = FuelCardForm()
    return render(request, 'vehicles/fuel_card_form.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.is_authenticated and u.role == 'manager')
def fuel_card_update_view(request, pk):
    fuel_card = get_object_or_404(FuelCard, pk=pk)
    if request.method == 'POST':
        form = FuelCardForm(request.POST, instance=fuel_card)
        if form.is_valid():
            form.save()
            return redirect('fuel_card_list')
    else:
        form = FuelCardForm(instance=fuel_card)
    return render(request, 'vehicles/fuel_card_form.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.is_authenticated and u.role == 'manager')
def fuel_card_delete_view(request, pk):
    fuel_card = get_object_or_404(FuelCard, pk=pk)
    if request.method == 'POST':
        fuel_card.delete()
        return redirect('fuel_card_list')
    return render(request, 'vehicles/fuel_card_confirm_delete.html', {'fuel_card': fuel_card})

def is_employee(user):
    return user.is_authenticated and user.role == 'employee'

@login_required
@user_passes_test(is_employee)
def trip_report_edit_view(request, pk):
    trip_report = get_object_or_404(TripReport, pk=pk, trip_request__user=request.user)
    if request.method == 'POST':
        form = TripReportForm(request.POST, instance=trip_report)
        if form.is_valid():
            form.save()
            messages.success(request, "Trip report updated successfully.")
            return redirect('trip_request_employee_list')
    else:
        form = TripReportForm(instance=trip_report)
    return render(request, 'vehicles/trip_report_form.html', {'form': form, 'trip_report': trip_report})

def is_manager(user):
    return user.is_authenticated and user.role == 'manager'

@login_required
@user_passes_test(is_manager)
def service_order_create_view(request):
    if request.method == 'POST':
        form = ServiceOrderForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Service order created successfully.")
            return redirect('service_order_list')
    else:
        form = ServiceOrderForm()
    return render(request, 'vehicles/service_order_form.html', {'form': form})

from django.utils import timezone

@login_required
@user_passes_test(is_manager)
def service_order_list_view(request):
    service_orders = ServiceOrder.objects.all()
    return render(request, 'vehicles/service_order_list.html', {'service_orders': service_orders})

@login_required
@user_passes_test(is_manager)
def service_order_update_view(request, pk):
    service_order = get_object_or_404(ServiceOrder, pk=pk)
    now = timezone.now().date()
    if service_order.date_going <= now <= service_order.date_coming_back:
        messages.error(request, "Cannot edit a service order during its duration.")
        return redirect('service_order_list')
    if request.method == 'POST':
        form = ServiceOrderForm(request.POST, request.FILES, instance=service_order)
        if form.is_valid():
            form.save()
            messages.success(request, "Service order updated successfully.")
            return redirect('service_order_list')
    else:
        form = ServiceOrderForm(instance=service_order)
    return render(request, 'vehicles/service_order_form.html', {'form': form})

@login_required
@user_passes_test(is_manager)
def service_order_delete_view(request, pk):
    service_order = get_object_or_404(ServiceOrder, pk=pk)
    now = timezone.now().date()
    if service_order.date_going <= now <= service_order.date_coming_back:
        messages.error(request, "Cannot delete a service order during its duration.")
        return redirect('service_order_list')
    if request.method == 'POST':
        service_order.delete()
        messages.success(request, "Service order deleted successfully.")
        return redirect('service_order_list')
    return render(request, 'vehicles/service_order_confirm_delete.html', {'service_order': service_order})

@login_required
@user_passes_test(is_manager)
def service_order_detail_view(request, pk):
    service_order = get_object_or_404(ServiceOrder, pk=pk)
    return render(request, 'vehicles/service_order_detail.html', {'service_order': service_order})

@login_required
@user_passes_test(is_manager)
def service_list_view(request):
    services = Service.objects.all()
    return render(request, 'vehicles/service_list.html', {'services': services})

@login_required
@user_passes_test(is_manager)
def service_create_view(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Service created successfully.")
            return redirect('service_list')
    else:
        form = ServiceForm()
    return render(request, 'vehicles/service_form.html', {'form': form})

@login_required
@user_passes_test(is_manager)
def service_update_view(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            messages.success(request, "Service updated successfully.")
            return redirect('service_list')
    else:
        form = ServiceForm(instance=service)
    return render(request, 'vehicles/service_form.html', {'form': form})

@login_required
@user_passes_test(is_manager)
def service_delete_view(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        service.delete()
        messages.success(request, "Service deleted successfully.")
        return redirect('service_list')
    return render(request, 'vehicles/service_confirm_delete.html', {'service': service})

def is_employee(user):
    return user.is_authenticated and user.role == 'employee'

@login_required
@user_passes_test(is_manager)
def trip_report_list_view(request):
    trip_reports = TripReport.objects.all()
    return render(request, 'vehicles/trip_report_list.html', {'trip_reports': trip_reports})

@login_required
@user_passes_test(is_manager)
def driver_list_view(request):
    drivers = Driver.objects.all()
    return render(request, 'vehicles/driver_list.html', {'drivers': drivers})

@login_required
@user_passes_test(is_manager)
def driver_create_view(request):
    if request.method == 'POST':
        form = DriverForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Driver added successfully.")
            return redirect('driver_list')
    else:
        form = DriverForm()
    return render(request, 'vehicles/driver_form.html', {'form': form})

@login_required
@user_passes_test(is_manager)
def driver_update_view(request, pk):
    driver = get_object_or_404(Driver, pk=pk)
    if request.method == 'POST':
        form = DriverForm(request.POST, instance=driver)
        if form.is_valid():
            form.save()
            messages.success(request, "Driver updated successfully.")
            return redirect('driver_list')
    else:
        form = DriverForm(instance=driver)
    return render(request, 'vehicles/driver_form.html', {'form': form})

@login_required
@user_passes_test(is_manager)
def driver_delete_view(request, pk):
    driver = get_object_or_404(Driver, pk=pk)
    if request.method == 'POST':
        driver.delete()
        messages.success(request, "Driver deleted successfully.")
        return redirect('driver_list')
    return render(request, 'vehicles/driver_confirm_delete.html', {'driver': driver})

@login_required
@user_passes_test(is_manager)
def trip_report_detail_view(request, pk):
    trip_report = get_object_or_404(TripReport, pk=pk)
    return render(request, 'vehicles/trip_report_detail.html', {'trip_report': trip_report})

@login_required
@user_passes_test(is_manager)
def vehicle_create_view(request):
    if request.method == 'POST':
        form = VehicleForm(request.POST)
        if form.is_valid():
            vehicle = form.save(commit=False)
            vehicle.status = 'free'
            vehicle.save()
            form.save_m2m()
            return redirect('vehicle_list')
    else:
        form = VehicleForm()
    return render(request, 'vehicles/vehicle_form.html', {'form': form})

@login_required
@user_passes_test(is_manager)
def vehicle_update_view(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    if request.method == 'POST':
        form = VehicleForm(request.POST, instance=vehicle)
        if form.is_valid():
            form.save()
            return redirect('vehicle_list')
    else:
        form = VehicleForm(instance=vehicle)
    return render(request, 'vehicles/vehicle_form.html', {'form': form})

@login_required
@user_passes_test(is_manager)
def vehicle_list_view(request):
    vehicles = Vehicle.objects.all()
    return render(request, 'vehicles/vehicle_list.html', {'vehicles': vehicles})

@login_required
@user_passes_test(is_manager)
def vehicle_delete_view(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    if request.method == 'POST':
        vehicle.delete()
        return redirect('vehicle_list')
    return render(request, 'vehicles/vehicle_confirm_delete.html', {'vehicle': vehicle})


@login_required
@user_passes_test(is_employee)
def trip_report_create_view(request, trip_request_id):
    trip_request = get_object_or_404(MissionOrder, pk=trip_request_id, user=request.user)
    vehicle = trip_request.vehicle
    if request.method == 'POST':
        form = TripReportForm(request.POST)
        if form.is_valid():
            trip_report = form.save(commit=False)
            trip_report.trip_request = trip_request
            # Set old mileage from vehicle's current mileage
            trip_report.old_mileage = vehicle.mileage if vehicle else None
            # Set fuel_filled from trip_request fuel_used
            trip_report.fuel_filled = trip_request.fuel_used
            trip_report.save()
            # Update the related vehicle's mileage
            if vehicle:
                vehicle.mileage = trip_report.new_mileage
                vehicle.save()
            # Update trip request status to 'reported'
            trip_request.status = 'reported'
            trip_request.save()
            messages.success(request, "Trip report submitted successfully.")
            return redirect('trip_request_employee_list')
        else:
            # Pass form errors explicitly to template
            return render(request, 'vehicles/trip_report_form.html', {'form': form, 'trip_request': trip_request, 'form_errors': form.errors})
    else:
        form = TripReportForm()
    return render(request, 'vehicles/trip_report_form.html', {'form': form, 'trip_request': trip_request})

@login_required
@user_passes_test(is_employee)
def trip_request_delete_view(request, pk):
    trip_request = get_object_or_404(MissionOrder, pk=pk, user=request.user)
    if trip_request.status != 'pending':
        return redirect('trip_request_employee_list')
    if request.method == 'POST':
        trip_request.delete()
        return redirect('trip_request_employee_list')
    return render(request, 'vehicles/trip_request_confirm_delete.html', {'trip_request': trip_request})

@login_required
@user_passes_test(is_employee)
def trip_request_employee_list_view(request):
    trip_requests = MissionOrder.objects.filter(user=request.user)
    return render(request, 'vehicles/trip_request_employee_list.html', {'trip_requests': trip_requests})

@login_required
@user_passes_test(is_manager)
def fuel_card_list_view(request):
    fuel_cards = FuelCard.objects.all()
    return render(request, 'vehicles/fuel_card_list.html', {'fuel_cards': fuel_cards})

from django.http import JsonResponse

@login_required
def vehicles_by_mission_view(request, mission_id):
    mission = get_object_or_404(Mission, pk=mission_id)
    vehicles = Vehicle.objects.filter(mission_type=mission)
    vehicles_data = [{'id': v.id, 'name': str(v)} for v in vehicles]
    return JsonResponse({'vehicles': vehicles_data})

@login_required
@user_passes_test(is_employee)
def trip_request_create_view(request):
    mission_id = None
    if request.method == 'POST':
        mission_id = request.POST.get('mission')
        mission = None
        if mission_id:
            mission = get_object_or_404(Mission, pk=mission_id)
        form = TripRequestForm(request.POST, request.FILES, mission=mission)
        if form.is_valid():
            trip_request = form.save(commit=False)
            trip_request.user = request.user
            # Since vehicle is removed from form, set vehicle to None or handle accordingly
            trip_request.vehicle = None
            trip_request.status = 'pending'
            trip_request.save()
            return redirect('home')
    else:
        mission_id = request.GET.get('mission')
        mission = None
        if mission_id:
            mission = get_object_or_404(Mission, pk=mission_id)
        form = TripRequestForm(mission=mission)
    return render(request, 'vehicles/trip_request_form.html', {'form': form})

@login_required
@user_passes_test(is_manager)
def trip_request_list_view(request):
    trip_requests = MissionOrder.objects.all()
    return render(request, 'vehicles/trip_request_list.html', {'trip_requests': trip_requests})

from .forms import MissionApprovalForm

@login_required
@user_passes_test(is_manager)
def trip_request_approve_view(request, pk):
    # Redirect to approval form for vehicle assignment and fuel consumption
    return redirect('trip_request_approval', pk=pk)

@login_required
@user_passes_test(is_manager)
def trip_request_approval_view(request, pk):
    trip_request = get_object_or_404(MissionOrder, pk=pk)
    if request.method == 'POST':
        form = MissionApprovalForm(request.POST, instance=trip_request)
        if form.is_valid():
            trip_request = form.save(commit=False)
            trip_request.status = 'approved'
            # Save fuel consumed to fuel_used field
            fuel_used = form.cleaned_data.get('fuel_consumed')
            trip_request.fuel_used = fuel_used
            trip_request.save()
            vehicle = trip_request.vehicle
            if vehicle and vehicle.department and vehicle.department.fuel_card and vehicle.fuel_card and fuel_used:
                department_fuel_card = vehicle.department.fuel_card
                vehicle_fuel_card = vehicle.fuel_card
                # Deduct fuel_used from department fuel card balance
                department_fuel_card.balance = max(department_fuel_card.balance - fuel_used, 0)
                department_fuel_card.save()
                # Add fuel_used to vehicle fuel card balance
                vehicle_fuel_card.balance += fuel_used
                vehicle_fuel_card.save()
            return redirect('trip_request_list')
    else:
        form = MissionApprovalForm(instance=trip_request)
    return render(request, 'vehicles/trip_request_approval_form.html', {'form': form, 'trip_request': trip_request})

@login_required
@user_passes_test(is_manager)
def trip_request_reject_view(request, pk):
    trip_request = get_object_or_404(MissionOrder, pk=pk)
    trip_request.status = 'rejected'
    trip_request.save()
    return redirect('trip_request_list')

@login_required
@user_passes_test(is_employee)
def trip_request_edit_view(request, pk):
    trip_request = get_object_or_404(MissionOrder, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TripRequestForm(request.POST, instance=trip_request)
        if form.is_valid():
            form.save()
            return redirect('trip_request_employee_list')
    else:
        form = TripRequestForm(instance=trip_request)
    return render(request, 'vehicles/trip_request_form.html', {'form': form})

@login_required
@user_passes_test(is_manager)
def trip_request_log_view(request):
    trip_requests = MissionOrder.objects.all()
    return render(request, 'vehicles/trip_request_log.html', {'trip_requests': trip_requests})

@login_required
@user_passes_test(is_manager)
def mission_list_view(request):
    missions = Mission.objects.all()
    return render(request, 'vehicles/mission_list.html', {'missions': missions})

@login_required
@user_passes_test(is_manager)
def mission_add_view(request):
    if request.method == 'POST':
        form = MissionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('mission_list')
    else:
        form = MissionForm()
    return render(request, 'vehicles/mission_form.html', {'form': form})

@login_required
@user_passes_test(is_manager)
def mission_order_create_view(request):
    if request.method == 'POST':
        form = MissionOrderManagerForm(request.POST, request.FILES)
        if form.is_valid():
            mission_order = form.save(commit=False)
            mission_order.status = 'approved'
            mission_order.save()
            fuel_used = mission_order.fuel_used
            vehicle = mission_order.vehicle
            if vehicle and vehicle.department and vehicle.department.fuel_card and vehicle.fuel_card and fuel_used:
                department_fuel_card = vehicle.department.fuel_card
                vehicle_fuel_card = vehicle.fuel_card
                # Deduct fuel_used from department fuel card balance
                department_fuel_card.balance = max(department_fuel_card.balance - fuel_used, 0)
                department_fuel_card.save()
                # Add fuel_used to vehicle fuel card balance
                vehicle_fuel_card.balance += fuel_used
                vehicle_fuel_card.save()
            return redirect('trip_request_list')
    else:
        form = MissionOrderManagerForm()
    return render(request, 'vehicles/mission_order_form.html', {'form': form})

@login_required
@user_passes_test(is_manager)
def mission_update_view(request, pk):
    mission = get_object_or_404(Mission, pk=pk)
    if request.method == 'POST':
        form = MissionForm(request.POST, instance=mission)
        if form.is_valid():
            form.save()
            return redirect('mission_list')
    else:
        form = MissionForm(instance=mission)
    return render(request, 'vehicles/mission_form.html', {'form': form})

@login_required
@user_passes_test(is_manager)
def mission_delete_view(request, pk):
    mission = get_object_or_404(Mission, pk=pk)
    if request.method == 'POST':
        mission.delete()
        return redirect('mission_list')
    return render(request, 'vehicles/mission_confirm_delete.html', {'mission': mission})

@login_required
@user_passes_test(is_manager)
def vehicle_model_list_view(request):
    vehicle_models = VehicleModel.objects.all()
    return render(request, 'vehicles/vehicle_model_list.html', {'models': vehicle_models})

@login_required
@user_passes_test(is_manager)
def vehicle_model_create_view(request):
    if request.method == 'POST':
        form = VehicleModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('vehicle_model_list')
    else:
        form = VehicleModelForm()
    return render(request, 'vehicles/vehicle_model_form.html', {'form': form})

@login_required
@user_passes_test(is_manager)
def vehicle_model_update_view(request, pk):
    vehicle_model = get_object_or_404(VehicleModel, pk=pk)
    if request.method == 'POST':
        form = VehicleModelForm(request.POST, instance=vehicle_model)
        if form.is_valid():
            form.save()
            return redirect('vehicle_model_list')
    else:
        form = VehicleModelForm(instance=vehicle_model)
    return render(request, 'vehicles/vehicle_model_form.html', {'form': form})

@login_required
@user_passes_test(is_manager)
def vehicle_model_delete_view(request, pk):
    vehicle_model = get_object_or_404(VehicleModel, pk=pk)
    if request.method == 'POST':
        vehicle_model.delete()
        return redirect('vehicle_model_list')
    return render(request, 'vehicles/vehicle_model_confirm_delete.html', {'vehicle_model': vehicle_model})

@login_required
@user_passes_test(is_manager)
def fuel_card_create_view(request):
    if request.method == 'POST':
        form = FuelCardForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('fuel_card_list')
    else:
        form = FuelCardForm()
    return render(request, 'vehicles/fuel_card_form.html', {'form': form})

@login_required
@user_passes_test(is_manager)
def fuel_card_update_view(request, pk):
    fuel_card = get_object_or_404(FuelCard, pk=pk)
    if request.method == 'POST':
        form = FuelCardForm(request.POST, instance=fuel_card)
        if form.is_valid():
            form.save()
            return redirect('fuel_card_list')
    else:
        form = FuelCardForm(instance=fuel_card)
    return render(request, 'vehicles/fuel_card_form.html', {'form': form})

@login_required
@user_passes_test(is_manager)
def fuel_card_delete_view(request, pk):
    fuel_card = get_object_or_404(FuelCard, pk=pk)
    if request.method == 'POST':
        fuel_card.delete()
        return redirect('fuel_card_list')
    return render(request, 'vehicles/fuel_card_confirm_delete.html', {'fuel_card': fuel_card})
