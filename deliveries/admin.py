from django.contrib import admin
from .models import Delivery, DeliveryFee, DeliveryRating

@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = ['id', 'donation', 'receiver', 'volunteer', 'status', 'distance_km', 
                    'otp_verified', 'requested_at']
    list_filter = ['status', 'otp_verified']
    search_fields = ['donation__food_title', 'receiver__username', 'volunteer__username']
    date_hierarchy = 'requested_at'
    readonly_fields = ['delivery_otp', 'requested_at', 'assigned_at', 'picked_up_at', 
                      'delivered_at', 'completed_at']

@admin.register(DeliveryFee)
class DeliveryFeeAdmin(admin.ModelAdmin):
    list_display = ['delivery', 'total_fee', 'volunteer_earning', 'platform_commission', 
                    'is_paid', 'created_at']
    list_filter = ['is_paid']
    search_fields = ['delivery__id']
    readonly_fields = ['subtotal', 'total_fee', 'volunteer_earning', 'platform_commission']

@admin.register(DeliveryRating)
class DeliveryRatingAdmin(admin.ModelAdmin):
    list_display = ['delivery', 'rated_by', 'rating', 'created_at']
    list_filter = ['rating']
    search_fields = ['delivery__id', 'rated_by__username']
    date_hierarchy = 'created_at'
