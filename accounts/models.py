from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('employee', 'Employee'),
        ('manager', 'Manager'),
    )
    department = models.CharField(max_length=100, blank=True, null=True)
    cin = models.CharField(max_length=20, unique=False, null=True, blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='employee')

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        # Automatically assign admin role if user is superuser
        if self.is_superuser:
            self.role = 'admin'
        super().save(*args, **kwargs)
