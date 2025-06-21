from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import CustomUser
from vehicles.models import Vehicle

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'employee'  
            user.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

@login_required
def home_view(request):
    available_vehicles_count = Vehicle.objects.filter(status='free').count()
    context = {
        'available_vehicles_count': available_vehicles_count,
        'user_role': request.user.role,
        'user_obj': request.user,
    }
    return render(request, 'accounts/home.html', context)

def logout_view(request):
    logout(request)
    return redirect('login')

def is_admin_user(user):
    return user.is_superuser or user.role == 'admin'

@login_required
@user_passes_test(is_admin_user)
def custom_change_roles_view(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        new_role = request.POST.get('role')
        try:
            user = CustomUser.objects.get(pk=user_id)
            user.role = new_role
            user.save()
            messages.success(request, f"Role for user {user.username} updated to {new_role}.")
        except CustomUser.DoesNotExist:
            messages.error(request, "User not found.")
        return redirect('change_roles')

    users = CustomUser.objects.all()
    roles = dict(CustomUser.ROLE_CHOICES)
    context = {
        'users': users,
        'roles': roles,
    }
    return render(request, 'accounts/change_roles.html', context)

def about_view(request):
    return render(request, 'accounts/about.html')

def deals_view(request):
    return render(request, 'accounts/deals.html')

def reservation_view(request):
    return render(request, 'accounts/reservation.html')
