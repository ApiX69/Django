from django import forms
from .models import Vehicle, VehicleModel, Mission, MissionOrder, FuelCard, TripReport, Driver, ServiceOrder, Service, Department

class DriverForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ['first_name', 'last_name', 'cin', 'status']

class MissionOrderManagerForm(forms.ModelForm):
    class Meta:
        model = MissionOrder
        fields = ['user', 'vehicle', 'mission', 'date_going', 'date_coming_back', 'motif', 'destination', 'fuel_used', 'file']
        widgets = {
            'date_going': forms.DateInput(attrs={'type': 'date'}),
            'date_coming_back': forms.DateInput(attrs={'type': 'date'}),
            'motif': forms.Textarea(attrs={'rows': 4}),
            'fuel_used': forms.NumberInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Optionally filter vehicles to those available or other logic
        self.fields['vehicle'].queryset = Vehicle.objects.filter(status='free')
        for field_name, field in self.fields.items():
            existing_classes = field.widget.attrs.get('class', '')
            classes = existing_classes + ' form-control'
            field.widget.attrs['class'] = classes.strip()

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        exclude = ['status']
        fields = ['model', 'year', 'license_plate', 'horsepower', 'mileage', 'date_bought', 'fuel_card', 'department']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter fuel_card queryset to only include Secondary type fuel cards not assigned to other vehicles except current instance
        if self.instance and self.instance.pk:
            assigned_cards = Vehicle.objects.exclude(pk=self.instance.pk).values_list('fuel_card', flat=True)
            self.fields['fuel_card'].queryset = FuelCard.objects.filter(type='Secondary').exclude(id__in=assigned_cards)
        else:
            assigned_cards = Vehicle.objects.values_list('fuel_card', flat=True)
            self.fields['fuel_card'].queryset = FuelCard.objects.filter(type='Secondary').exclude(id__in=assigned_cards)
        for field_name, field in self.fields.items():
            existing_classes = field.widget.attrs.get('class', '')
            classes = existing_classes + ' form-control'
            field.widget.attrs['class'] = classes.strip()
    

class VehicleModelForm(forms.ModelForm):
    class Meta:
        model = VehicleModel
        fields = '__all__'

class MissionForm(forms.ModelForm):
    class Meta:
        model = Mission
        fields = '__all__'

class TripRequestForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        mission = kwargs.pop('mission', None)
        super().__init__(*args, **kwargs)
        self.fields['vehicle'].queryset = Vehicle.objects.filter(status='free')
        for field_name, field in self.fields.items():
            existing_classes = field.widget.attrs.get('class', '')
            classes = existing_classes + ' form-control'
            field.widget.attrs['class'] = classes.strip()

    class Meta:
        model = MissionOrder
        exclude = ['user', 'status']
        widgets = {
            'date_going': forms.DateInput(attrs={'type': 'date'}),
            'date_coming_back': forms.DateInput(attrs={'type': 'date'}),
            'motif': forms.Textarea(attrs={'rows': 4}),
        }
        fields = ['mission', 'vehicle', 'date_going', 'date_coming_back', 'destination', 'motif', 'file']

class FuelCardForm(forms.ModelForm):
    TYPE_CHOICES = [
        ('Primary', 'Primary'),
        ('Secondary', 'Secondary'),
    ]
    type = forms.ChoiceField(choices=TYPE_CHOICES)

    class Meta:
        model = FuelCard
        fields = '__all__'

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'fuel_card']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Limit fuel_card choices to Primary type only and exclude already assigned fuel cards except current instance
        assigned_fuel_cards = Department.objects.exclude(pk=self.instance.pk).values_list('fuel_card', flat=True)
        self.fields['fuel_card'].queryset = FuelCard.objects.filter(type='Primary').exclude(id__in=assigned_fuel_cards)

    def clean_fuel_card(self):
        fuel_card = self.cleaned_data.get('fuel_card')
        if Department.objects.filter(fuel_card=fuel_card).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("This fuel card is already assigned to another department.")
        return fuel_card

class TripReportForm(forms.ModelForm):
    class Meta:
        model = TripReport
        fields = ['report_text', 'new_mileage', 'issue_occurred', 'issue_detail']
        widgets = {
            'report_text': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'new_mileage': forms.NumberInput(attrs={'class': 'form-control'}),
            'issue_occurred': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'issue_detail': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.widget.attrs.get('class') is None:
                field.widget.attrs['class'] = 'form-control'
            elif 'form-control' not in field.widget.attrs['class']:
                field.widget.attrs['class'] += ' form-control'

class MissionApprovalForm(forms.ModelForm):
    vehicle = forms.ModelChoiceField(queryset=Vehicle.objects.filter(status='free'), required=True)
    fuel_consumed = forms.DecimalField(max_digits=6, decimal_places=2, required=True, help_text="Fuel to be consumed by the vehicle")

    class Meta:
        model = MissionOrder
        fields = ['vehicle']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class ServiceOrderForm(forms.ModelForm):
    class Meta:
        model = ServiceOrder
        fields = ['vehicle', 'service', 'date_going', 'date_coming_back', 'destination', 'driver', 'fuel_used', 'motif', 'status', 'file']
        widgets = {
            'date_going': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'date_coming_back': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'destination': forms.TextInput(attrs={'class': 'form-control'}),
            'fuel_used': forms.NumberInput(attrs={'class': 'form-control'}),
            'motif': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.widget.attrs.get('class') is None:
                field.widget.attrs['class'] = 'form-control'
            elif 'form-control' not in field.widget.attrs['class']:
                field.widget.attrs['class'] += ' form-control'

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            existing_classes = field.widget.attrs.get('class', '')
            classes = existing_classes + ' form-control'
            field.widget.attrs['class'] = classes.strip()
