# 🚀 Phase 1: Foundation & Architecture - Implementation Guide

## 📋 Overview
This phase establishes the foundation for enterprise transformation. We'll restructure the Django project into modular apps, extend the database schema, and implement role-based access control.

---

## 🎯 Phase 1 Goals

1. ✅ Modular Django app structure
2. ✅ Extended database models
3. ✅ Role-based access control
4. ✅ Subscription foundation
5. ✅ Geolocation support

**Timeline:** 2 weeks
**Priority:** CRITICAL

---

## 📁 Step 1: Create Django Apps Structure

### Commands to Run:

```bash
# Navigate to project directory
cd food_donation_project

# Create new Django apps
python manage.py startapp users
python manage.py startapp subscriptions
python manage.py startapp volunteers
python manage.py startapp wallet
python manage.py startapp deliveries
python manage.py startapp analytics
python manage.py startapp chatbot
python manage.py startapp notifications
python manage.py startapp sponsors
```

### Update settings.py:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Existing app
    'donations',
    
    # New enterprise apps
    'users',
    'subscriptions',
    'volunteers',
    'wallet',
    'deliveries',
    'analytics',
    'chatbot',
    'notifications',
    'sponsors',
]
```

---

## 🗄️ Step 2: Extended Database Models

### 2.1 Users App - Extended User Model

**File:** `users/models.py`

```python
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class CustomUser(AbstractUser):
    """Extended user model with enterprise features"""
    
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('donor_restaurant', 'Donor - Restaurant'),
        ('donor_individual', 'Donor - Individual'),
        ('receiver_ngo', 'Receiver - NGO'),
        ('receiver_shelter', 'Receiver - Shelter'),
        ('volunteer', 'Volunteer - Delivery Partner'),
        ('corporate', 'Corporate Sponsor'),
    ]
    
    # Basic Info
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    
    # Geolocation
    address = models.TextField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    
    # Verification
    is_verified = models.BooleanField(default=False)
    verification_document = models.FileField(upload_to='verifications/', null=True, blank=True)
    
    # Subscription (will link to subscriptions app)
    current_subscription = models.ForeignKey('subscriptions.UserSubscription', 
                                            on_delete=models.SET_NULL, 
                                            null=True, blank=True,
                                            related_name='user_subscription')
    
    # Timestamps
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
        """Get current subscription tier"""
        if self.current_subscription and self.current_subscription.is_active():
            return self.current_subscription.plan.tier
        return 'free'
    
    def has_feature(self, feature_name):
        """Check if user has access to a feature"""
        tier = self.get_subscription_tier()
        from subscriptions.models import SubscriptionPlan
        return SubscriptionPlan.has_feature(tier, feature_name)
```

---

### 2.2 Subscriptions App - Plans & Billing

**File:** `subscriptions/models.py`

```python
from django.db import models
from django.utils import timezone
from datetime import timedelta

class SubscriptionPlan(models.Model):
    """Subscription plans with feature matrix"""
    
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
    
    # Feature Limits
    max_donations_per_month = models.IntegerField(default=10)
    max_requests_per_month = models.IntegerField(default=10)
    max_storage_mb = models.IntegerField(default=100)
    api_rate_limit = models.IntegerField(default=100)  # requests per hour
    
    # Feature Flags
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
    
    @staticmethod
    def has_feature(tier, feature_name):
        """Check if a tier has a specific feature"""
        try:
            plan = SubscriptionPlan.objects.get(tier=tier)
            return getattr(plan, f'has_{feature_name}', False)
        except SubscriptionPlan.DoesNotExist:
            return False


class UserSubscription(models.Model):
    """User's active subscription"""
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
        ('pending', 'Pending Payment'),
    ]
    
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='subscriptions')
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
        """Check if subscription is currently active"""
        return (self.status == 'active' and 
                self.start_date <= timezone.now() <= self.end_date)
    
    def days_remaining(self):
        """Calculate days remaining"""
        if self.is_active():
            return (self.end_date - timezone.now()).days
        return 0
    
    def extend_subscription(self, months=1):
        """Extend subscription by months"""
        self.end_date = self.end_date + timedelta(days=30*months)
        self.save()


class BillingHistory(models.Model):
    """Payment and billing records"""
    
    TRANSACTION_TYPE_CHOICES = [
        ('subscription', 'Subscription Payment'),
        ('upgrade', 'Plan Upgrade'),
        ('renewal', 'Subscription Renewal'),
        ('refund', 'Refund'),
    ]
    
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)
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
```

---

### 2.3 Volunteers App - Logistics Management

**File:** `volunteers/models.py`

```python
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class VolunteerProfile(models.Model):
    """Volunteer delivery partner profile"""
    
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('busy', 'Busy'),
        ('offline', 'Offline'),
    ]
    
    VEHICLE_CHOICES = [
        ('bike', 'Bike'),
        ('scooter', 'Scooter'),
        ('car', 'Car'),
        ('van', 'Van'),
    ]
    
    user = models.OneToOneField('users.CustomUser', on_delete=models.CASCADE, related_name='volunteer_profile')
    
    # Availability
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='offline')
    is_available = models.BooleanField(default=False)
    
    # Location (real-time)
    current_latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    current_longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    last_location_update = models.DateTimeField(null=True, blank=True)
    
    # Capacity
    vehicle_type = models.CharField(max_length=20, choices=VEHICLE_CHOICES)
    max_delivery_capacity = models.IntegerField(default=5)  # items per trip
    service_radius_km = models.IntegerField(default=10)
    
    # Performance
    total_deliveries = models.IntegerField(default=0)
    successful_deliveries = models.IntegerField(default=0)
    cancelled_deliveries = models.IntegerField(default=0)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00,
                                        validators=[MinValueValidator(0), MaxValueValidator(5)])
    total_ratings = models.IntegerField(default=0)
    
    # Earnings
    total_earnings = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    pending_payout = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    # Verification
    is_verified = models.BooleanField(default=False)
    driving_license = models.FileField(upload_to='volunteer_docs/', null=True)
    vehicle_registration = models.FileField(upload_to='volunteer_docs/', null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'volunteer_profiles'
        indexes = [
            models.Index(fields=['status', 'is_available']),
            models.Index(fields=['current_latitude', 'current_longitude']),
        ]
    
    def __str__(self):
        return f"{self.user.full_name} - {self.get_status_display()}"
    
    def update_location(self, lat, lng):
        """Update volunteer's current location"""
        from django.utils import timezone
        self.current_latitude = lat
        self.current_longitude = lng
        self.last_location_update = timezone.now()
        self.save()
    
    def calculate_success_rate(self):
        """Calculate delivery success rate"""
        if self.total_deliveries == 0:
            return 0
        return (self.successful_deliveries / self.total_deliveries) * 100


class VolunteerEarnings(models.Model):
    """Track volunteer earnings per delivery"""
    
    volunteer = models.ForeignKey(VolunteerProfile, on_delete=models.CASCADE, related_name='earnings')
    delivery = models.ForeignKey('deliveries.Delivery', on_delete=models.CASCADE)
    
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    platform_commission = models.DecimalField(max_digits=10, decimal_places=2)
    net_earnings = models.DecimalField(max_digits=10, decimal_places=2)
    
    status = models.CharField(max_length=20, default='pending')  # pending, paid
    payout_date = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'volunteer_earnings'
        ordering = ['-created_at']
```

---

## 🎯 Step 3: Role-Based Access Control

### Create Decorators

**File:** `users/decorators.py`

```python
from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.http import JsonResponse

def role_required(*allowed_roles):
    """Decorator to check if user has required role"""
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            
            if request.user.role not in allowed_roles:
                messages.error(request, 'You do not have permission to access this page.')
                return redirect('home')
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def subscription_required(tier='pro'):
    """Decorator to check subscription tier"""
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            
            user_tier = request.user.get_subscription_tier()
            tier_hierarchy = {'free': 0, 'pro': 1, 'enterprise': 2}
            
            if tier_hierarchy.get(user_tier, 0) < tier_hierarchy.get(tier, 0):
                messages.error(request, f'This feature requires {tier.title()} subscription.')
                return redirect('subscription_plans')
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def feature_required(feature_name):
    """Decorator to check if user has specific feature"""
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            
            if not request.user.has_feature(feature_name):
                messages.error(request, f'This feature is not available in your plan.')
                return redirect('subscription_plans')
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
```

---

## 📝 Implementation Checklist

### Week 1:
- [ ] Create all Django apps
- [ ] Update settings.py
- [ ] Create extended User model
- [ ] Create Subscription models
- [ ] Create Volunteer models
- [ ] Run migrations
- [ ] Test basic functionality

### Week 2:
- [ ] Implement role decorators
- [ ] Create subscription views
- [ ] Add geolocation fields
- [ ] Test role-based access
- [ ] Create admin interfaces
- [ ] Documentation

---

## 🚀 Next Steps

After completing Phase 1:
1. Move to Phase 2: Subscription & Monetization
2. Implement payment flow (DEMO mode)
3. Create subscription upgrade UI
4. Add feature gating throughout app

---

**Status:** Ready to implement
**Estimated Time:** 2 weeks
**Dependencies:** None
**Risk Level:** Low

