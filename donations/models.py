from django.db import models
from django.conf import settings

class Donation(models.Model):
    CATEGORY_CHOICES = [
        ('vegetarian', 'Vegetarian'),
        ('vegan', 'Vegan'),
        ('non_veg', 'Non-Vegetarian'),
        ('halal', 'Halal'),
        ('kosher', 'Kosher'),
        ('gluten_free', 'Gluten Free'),
        ('dairy_free', 'Dairy Free'),
        ('other', 'Other'),
    ]
    
    donor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='donations')
    food_title = models.CharField(max_length=255)
    description = models.TextField()
    quantity = models.CharField(max_length=100)
    pickup_location = models.CharField(max_length=500)
    
    pickup_latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    pickup_longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    
    expiry_date = models.DateField()
    food_image = models.ImageField(upload_to='donation_images/', null=True, blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')
    pickup_time_start = models.TimeField(null=True, blank=True)
    pickup_time_end = models.TimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.food_title
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['pickup_latitude', 'pickup_longitude']),
            models.Index(fields=['category']),
            models.Index(fields=['expiry_date']),
        ]


class Request(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    donation = models.ForeignKey(Donation, on_delete=models.CASCADE, related_name='requests')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='requests')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    is_read = models.BooleanField(default=False)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Request by {self.receiver.full_name} for {self.donation.food_title}"
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ['donation', 'receiver']
