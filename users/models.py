from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('donor_restaurant', 'Donor - Restaurant'),
        ('donor_individual', 'Donor - Individual'),
        ('receiver_ngo', 'Receiver - NGO'),
        ('receiver_shelter', 'Receiver - Shelter'),
        ('volunteer', 'Volunteer - Delivery Partner'),
        ('corporate', 'Corporate Sponsor'),
    ]
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    
    address = models.TextField(blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    
    is_verified = models.BooleanField(default=False)
    verification_document = models.FileField(upload_to='verifications/', null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'custom_users'
        indexes = [
            models.Index(fields=['role']),
            models.Index(fields=['latitude', 'longitude']),
            models.Index(fields=['is_verified']),
        ]
    
    def __str__(self):
        return f"{self.full_name} ({self.get_role_display()})"
    
    def get_subscription_tier(self):
        try:
            if hasattr(self, 'active_subscription') and self.active_subscription:
                if self.active_subscription.is_active():
                    return self.active_subscription.plan.tier
        except:
            pass
        return 'free'
    
    def has_feature(self, feature_name):
        tier = self.get_subscription_tier()
        from subscriptions.models import SubscriptionPlan
        try:
            plan = SubscriptionPlan.objects.get(tier=tier)
            return getattr(plan, f'has_{feature_name}', False)
        except:
            return False
