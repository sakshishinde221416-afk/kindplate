from django.contrib import admin
from .models import VolunteerProfile, VolunteerEarnings

@admin.register(VolunteerProfile)
class VolunteerProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'status', 'is_available', 'vehicle_type', 'total_deliveries', 
                    'average_rating', 'total_earnings', 'is_verified']
    list_filter = ['status', 'is_available', 'vehicle_type', 'is_verified']
    search_fields = ['user__username', 'user__full_name']
    readonly_fields = ['total_deliveries', 'successful_deliveries', 'cancelled_deliveries', 
                      'average_rating', 'total_ratings', 'total_earnings']

@admin.register(VolunteerEarnings)
class VolunteerEarningsAdmin(admin.ModelAdmin):
    list_display = ['volunteer', 'delivery', 'amount', 'net_earnings', 'status', 'created_at']
    list_filter = ['status']
    search_fields = ['volunteer__user__username']
    date_hierarchy = 'created_at'
