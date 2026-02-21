from django.db import models
from django.conf import settings

class PlatformMetrics(models.Model):
    date = models.DateField(unique=True)
    
    total_users = models.IntegerField(default=0)
    new_users = models.IntegerField(default=0)
    active_users = models.IntegerField(default=0)
    
    total_donations = models.IntegerField(default=0)
    new_donations = models.IntegerField(default=0)
    completed_donations = models.IntegerField(default=0)
    
    total_deliveries = models.IntegerField(default=0)
    successful_deliveries = models.IntegerField(default=0)
    cancelled_deliveries = models.IntegerField(default=0)
    
    total_volunteers = models.IntegerField(default=0)
    active_volunteers = models.IntegerField(default=0)
    
    meals_saved = models.IntegerField(default=0)
    
    revenue_subscriptions = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    revenue_deliveries = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    revenue_total = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'platform_metrics'
        ordering = ['-date']
    
    def __str__(self):
        return f"Metrics for {self.date}"


class UserActivity(models.Model):
    ACTIVITY_TYPE_CHOICES = [
        ('login', 'Login'),
        ('donation_created', 'Donation Created'),
        ('request_sent', 'Request Sent'),
        ('delivery_completed', 'Delivery Completed'),
        ('subscription_upgraded', 'Subscription Upgraded'),
        ('wallet_recharged', 'Wallet Recharged'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=30, choices=ACTIVITY_TYPE_CHOICES)
    description = models.TextField(blank=True)
    
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'user_activities'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'activity_type']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.user.full_name} - {self.get_activity_type_display()}"
