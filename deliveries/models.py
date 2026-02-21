from django.db import models
from django.conf import settings
from decimal import Decimal
import random
import string

class Delivery(models.Model):
    STATUS_CHOICES = [
        ('requested', 'Requested'),
        ('fee_calculated', 'Fee Calculated'),
        ('payment_confirmed', 'Payment Confirmed'),
        ('assigned', 'Assigned to Volunteer'),
        ('picked_up', 'Picked Up'),
        ('in_transit', 'In Transit'),
        ('delivered', 'Delivered'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    donation = models.ForeignKey('donations.Donation', on_delete=models.CASCADE, related_name='deliveries')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_deliveries')
    volunteer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='volunteer_deliveries')
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='requested')
    
    pickup_latitude = models.DecimalField(max_digits=9, decimal_places=6)
    pickup_longitude = models.DecimalField(max_digits=9, decimal_places=6)
    pickup_address = models.TextField()
    
    delivery_latitude = models.DecimalField(max_digits=9, decimal_places=6)
    delivery_longitude = models.DecimalField(max_digits=9, decimal_places=6)
    delivery_address = models.TextField()
    
    distance_km = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    
    delivery_otp = models.CharField(max_length=6, blank=True)
    otp_verified = models.BooleanField(default=False)
    
    pickup_photo = models.ImageField(upload_to='delivery_photos/', null=True, blank=True)
    delivery_photo = models.ImageField(upload_to='delivery_photos/', null=True, blank=True)
    
    requested_at = models.DateTimeField(auto_now_add=True)
    assigned_at = models.DateTimeField(null=True, blank=True)
    picked_up_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    notes = models.TextField(blank=True)
    cancellation_reason = models.TextField(blank=True)
    
    class Meta:
        db_table = 'deliveries'
        ordering = ['-requested_at']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['volunteer', 'status']),
            models.Index(fields=['receiver']),
        ]
    
    def __str__(self):
        return f"Delivery #{self.id} - {self.get_status_display()}"
    
    def generate_otp(self):
        self.delivery_otp = ''.join(random.choices(string.digits, k=6))
        self.save()
        return self.delivery_otp
    
    def verify_otp(self, otp):
        if self.delivery_otp == otp:
            self.otp_verified = True
            self.save()
            return True
        return False


class DeliveryFee(models.Model):
    delivery = models.OneToOneField(Delivery, on_delete=models.CASCADE, related_name='fee')
    
    base_fee = models.DecimalField(max_digits=10, decimal_places=2, default=20.00)
    distance_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    surge_multiplier = models.DecimalField(max_digits=3, decimal_places=2, default=1.00)
    
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    platform_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_fee = models.DecimalField(max_digits=10, decimal_places=2)
    
    volunteer_earning = models.DecimalField(max_digits=10, decimal_places=2)
    platform_commission = models.DecimalField(max_digits=10, decimal_places=2)
    
    is_paid = models.BooleanField(default=False)
    payment_transaction = models.ForeignKey('wallet.Transaction', on_delete=models.SET_NULL, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'delivery_fees'
    
    def __str__(self):
        return f"Fee for Delivery #{self.delivery.id} - ₹{self.total_fee}"
    
    @staticmethod
    def calculate_fee(distance_km, surge=1.0):
        base_fee = Decimal('20.00')
        distance_fee = Decimal(str(distance_km)) * Decimal('5.00')
        subtotal = (base_fee + distance_fee) * Decimal(str(surge))
        platform_fee = subtotal * Decimal('0.10')
        total_fee = subtotal + platform_fee
        volunteer_earning = subtotal * Decimal('0.90')
        platform_commission = subtotal * Decimal('0.10')
        
        return {
            'base_fee': base_fee,
            'distance_fee': distance_fee,
            'surge_multiplier': surge,
            'subtotal': subtotal,
            'platform_fee': platform_fee,
            'total_fee': total_fee,
            'volunteer_earning': volunteer_earning,
            'platform_commission': platform_commission,
        }


class DeliveryRating(models.Model):
    delivery = models.OneToOneField(Delivery, on_delete=models.CASCADE, related_name='rating')
    rated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    review = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'delivery_ratings'
    
    def __str__(self):
        return f"Rating for Delivery #{self.delivery.id} - {self.rating}★"
