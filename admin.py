from django.contrib import admin
from .models import CustomHost


@admin.register(CustomHost)
class CustomHostAdmin(admin.ModelAdmin):
    """
    Custom admin interface for CustomHost model
    """
    list_display = (
        'email', 'full_name', 'business_name', 'business_type', 
        'is_verified', 'is_active', 'date_joined'
    )
    list_filter = ('business_type', 'is_verified', 'is_active', 'date_joined', 'city', 'country')
    search_fields = ('email', 'full_name', 'business_name', 'phone_number', 'city')
    readonly_fields = ('date_joined', 'last_login')
    
    fieldsets = (
        (None, {
            'fields': ('username', 'email', 'password')
        }),
        ('Personal Info', {
            'fields': ('full_name', 'phone_number')
        }),
        ('Business Info', {
            'fields': ('business_name', 'business_license', 'business_type', 'bio')
        }),
        ('Address', {
            'fields': ('address', 'city', 'state', 'country', 'postal_code')
        }),
        ('Verification', {
            'fields': ('is_verified', 'verification_documents')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
        ('Additional', {
            'fields': ('profile_image',)
        }),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'full_name', 'phone_number', 'password1', 'password2'),
        }),
    )
    
    actions = ['verify_hosts', 'unverify_hosts']
    
    def verify_hosts(self, request, queryset):
        updated = queryset.update(is_verified=True)
        self.message_user(request, f'{updated} hosts were successfully verified.')
    verify_hosts.short_description = "Mark selected hosts as verified"
    
    def unverify_hosts(self, request, queryset):
        updated = queryset.update(is_verified=False)
        self.message_user(request, f'{updated} hosts were marked as unverified.')
    unverify_hosts.short_description = "Mark selected hosts as unverified"