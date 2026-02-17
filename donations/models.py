from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('donor', 'Donor'),
        ('receiver', 'Receiver'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    
    def __str__(self):
        return f"{self.full_name} ({self.role})"

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
    
    donor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='donations')
    food_title = models.CharField(max_length=255)
    description = models.TextField()
    quantity = models.CharField(max_length=100)
    pickup_location = models.CharField(max_length=500)
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

class Request(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    donation = models.ForeignKey(Donation, on_delete=models.CASCADE, related_name='requests')
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='requests')
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
