from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomHost(AbstractUser):
    """
    Custom host model for property owners/managers
    """
    # Business information
    business_name = models.CharField(max_length=255, blank=True)
    business_license = models.CharField(max_length=100, blank=True, help_text="Business license number")
    business_type = models.CharField(max_length=50, choices=[
        ('individual', 'Individual'),
        ('company', 'Company'),
        ('agency', 'Real Estate Agency'),
    ], default='individual')
    
    # Contact information
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    
    # Address information
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    
    # Verification status
    is_verified = models.BooleanField(default=False, help_text="Whether the host is verified by admin")
    verification_documents = models.TextField(blank=True, help_text="Notes about verification documents")
    
    # Additional info
    bio = models.TextField(blank=True, help_text="Host description/bio")
    profile_image = models.URLField(blank=True, help_text="URL to profile image")
    
    # Use email as the unique identifier for authentication
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'full_name', 'phone_number']
    
    class Meta:
        db_table = 'host_auth_customhost'
        verbose_name = 'Host'
        verbose_name_plural = 'Hosts'
    
    def __str__(self):
        return f"{self.business_name or self.full_name} ({self.email})"
    
    def get_full_name(self):
        return self.full_name
    
    def get_business_display_name(self):
        return self.business_name or self.full_name