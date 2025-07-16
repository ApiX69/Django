from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={"class": "form-control form-control-lg shadow-sm"}))
    region = forms.ChoiceField(choices=CustomUser.REGION_CHOICES, required=True, widget=forms.Select(attrs={"class": "form-control form-control-lg shadow-sm"}))
    cin = forms.CharField(max_length=20, required=True, widget=forms.TextInput(attrs={"class": "form-control form-control-lg shadow-sm"}))

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'region', 'cin', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({"class": "form-control form-control-lg shadow-sm"})
        self.fields['password1'].widget.attrs.update({"class": "form-control form-control-lg shadow-sm"})
        self.fields['password2'].widget.attrs.update({"class": "form-control form-control-lg shadow-sm"})

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={"class": "form-control form-control-lg shadow-sm"}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={"class": "form-control form-control-lg shadow-sm"}))
