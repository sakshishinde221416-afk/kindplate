from django.contrib import admin
from .models import PlatformMetrics, UserActivity

@admin.register(PlatformMetrics)
class PlatformMetricsAdmin(admin.ModelAdmin):
    list_display = ['date', 'total_users', 'new_users', 'total_donations', 'successful_deliveries', 
                    'meals_saved', 'revenue_total']
    list_filter = ['date']
    date_hierarchy = 'date'
    readonly_fields = ['created_at', 'updated_at']

@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    list_display = ['user', 'activity_type', 'created_at']
    list_filter = ['activity_type']
    search_fields = ['user__username', 'description']
    date_hierarchy = 'created_at'
