from django.contrib import admin
from .models import SubscriptionPlan, UserSubscription, BillingHistory

@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'tier', 'price_monthly', 'price_yearly', 'is_active']
    list_filter = ['tier', 'is_active']
    search_fields = ['name', 'description']

@admin.register(UserSubscription)
class UserSubscriptionAdmin(admin.ModelAdmin):
    list_display = ['user', 'plan', 'status', 'start_date', 'end_date', 'auto_renew']
    list_filter = ['status', 'plan', 'auto_renew']
    search_fields = ['user__username', 'user__email']
    date_hierarchy = 'start_date'

@admin.register(BillingHistory)
class BillingHistoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'transaction_type', 'amount', 'payment_status', 'created_at']
    list_filter = ['transaction_type', 'payment_status']
    search_fields = ['user__username', 'transaction_id', 'invoice_number']
    date_hierarchy = 'created_at'
