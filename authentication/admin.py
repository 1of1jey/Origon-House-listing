from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    """
    Custom admin interface for CustomUser model
    """
    model = CustomUser
    list_display = ('email', 'username', 'full_name', 'phone_number', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('is_staff', 'is_active', 'date_joined')
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('full_name', 'phone_number')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('full_name', 'phone_number', 'email')}),
    )
    search_fields = ('email', 'username', 'full_name', 'phone_number')
    ordering = ('email',)


admin.site.register(CustomUser, CustomUserAdmin)
