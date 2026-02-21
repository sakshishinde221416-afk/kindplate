from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.conf import settings

class SubscriptionPlan(models.Model):
    TIER_CHOICES = [
        ('free', 'Free'),
        ('pro', 'Pro'),
        ('enterprise', 'Enterprise'),
    ]
    
    tier = models.CharField(max_length=20, choices=TIER_CHOICES, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price_monthly = models.DecimalField(max_digits=10, decimal_places=2)
    price_yearly = models.DecimalField(max_digits=10, decimal_places=2)
    
    max_donations_per_month = models.IntegerField(default=10)
    max_requests_per_month = models.IntegerField(default=10)
    max_storage_mb = models.IntegerField(default=100)
    api_rate_limit = models.IntegerField(default=100)
    
    has_priority_matching = models.BooleanField(default=False)
    has_advanced_analytics = models.BooleanField(default=False)
    has_geo_radius_custom = models.BooleanField(default=False)
    has_volunteer_auto_assign = models.BooleanField(default=False)
    has_ai_chatbot = models.BooleanField(default=False)
    has_api_access = models.BooleanField(default=False)
    has_white_label = models.BooleanField(default=False)
    has_dedicated_support = models.BooleanField(default=False)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'subscription_plans'
        ordering = ['price_monthly']
    
    def __str__(self):
        return f"{self.name} (₹{self.price_monthly}/month)"


class UserSubscription(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
        ('pending', 'Pending Payment'),
    ]
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='active_subscription')
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.PROTECT)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    
    auto_renew = models.BooleanField(default=True)
    payment_method = models.CharField(max_length=50, default='demo')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'user_subscriptions'
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['end_date']),
        ]
    
    def __str__(self):
        return f"{self.user.full_name} - {self.plan.name}"
    
    def is_active(self):
        return (self.status == 'active' and 
                self.start_date <= timezone.now() <= self.end_date)
    
    def days_remaining(self):
        if self.is_active():
            return (self.end_date - timezone.now()).days
        return 0


class BillingHistory(models.Model):
    TRANSACTION_TYPE_CHOICES = [
        ('subscription', 'Subscription Payment'),
        ('upgrade', 'Plan Upgrade'),
        ('renewal', 'Subscription Renewal'),
        ('refund', 'Refund'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    subscription = models.ForeignKey(UserSubscription, on_delete=models.SET_NULL, null=True)
    
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='INR')
    
    payment_method = models.CharField(max_length=50, default='demo')
    transaction_id = models.CharField(max_length=100, unique=True)
    payment_status = models.CharField(max_length=20, default='completed')
    
    invoice_number = models.CharField(max_length=50, unique=True)
    invoice_pdf = models.FileField(upload_to='invoices/', null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'billing_history'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.full_name} - ₹{self.amount} - {self.transaction_type}"
