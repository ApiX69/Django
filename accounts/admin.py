from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.urls import path
from django.shortcuts import render, redirect
from django.template.response import TemplateResponse
from django.utils.html import format_html
from django.http import HttpResponseRedirect
from django import forms
from django.contrib import messages

from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'role', 'department', 'is_staff', 'is_active']
    list_filter = ['role', 'is_staff', 'is_active']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role', 'department')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('role', 'department')}),
    )

    # Add a custom admin view for changing user roles
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('change_roles/', self.admin_site.admin_view(self.change_roles_view), name='change_roles'),
        ]
        return custom_urls + urls

    def change_roles_view(self, request):
        if request.method == 'POST':
            user_id = request.POST.get('user_id')
            new_role = request.POST.get('role')
            try:
                user = CustomUser.objects.get(pk=user_id)
                user.role = new_role
                user.save()
                self.message_user(request, f"Role for user {user.username} updated to {new_role}.", messages.SUCCESS)
            except CustomUser.DoesNotExist:
                self.message_user(request, "User not found.", messages.ERROR)
            return HttpResponseRedirect(request.path)

        users = CustomUser.objects.all()
        roles = dict(CustomUser.ROLE_CHOICES)
        context = dict(
            self.admin_site.each_context(request),
            users=users,
            roles=roles,
        )
        return TemplateResponse(request, "admin/change_roles.html", context)

admin.site.register(CustomUser, CustomUserAdmin)
