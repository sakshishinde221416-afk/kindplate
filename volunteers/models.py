from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings

class VolunteerProfile(models.Model):
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
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='volunteer_profile')
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='offline')
    is_available = models.BooleanField(default=False)
    
    current_latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    current_longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    last_location_update = models.DateTimeField(null=True, blank=True)
    
    vehicle_type = models.CharField(max_length=20, choices=VEHICLE_CHOICES)
    max_delivery_capacity = models.IntegerField(default=5)
    service_radius_km = models.IntegerField(default=10)
    
    total_deliveries = models.IntegerField(default=0)
    successful_deliveries = models.IntegerField(default=0)
    cancelled_deliveries = models.IntegerField(default=0)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00,
                                        validators=[MinValueValidator(0), MaxValueValidator(5)])
    total_ratings = models.IntegerField(default=0)
    
    total_earnings = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    pending_payout = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
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
        from django.utils import timezone
        self.current_latitude = lat
        self.current_longitude = lng
        self.last_location_update = timezone.now()
        self.save()
    
    def calculate_success_rate(self):
        if self.total_deliveries == 0:
            return 0
        return (self.successful_deliveries / self.total_deliveries) * 100


class VolunteerEarnings(models.Model):
    volunteer = models.ForeignKey(VolunteerProfile, on_delete=models.CASCADE, related_name='earnings')
    delivery = models.ForeignKey('deliveries.Delivery', on_delete=models.CASCADE)
    
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    platform_commission = models.DecimalField(max_digits=10, decimal_places=2)
    net_earnings = models.DecimalField(max_digits=10, decimal_places=2)
    
    status = models.CharField(max_length=20, default='pending')
    payout_date = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'volunteer_earnings'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.volunteer.user.full_name} - ₹{self.net_earnings}"
