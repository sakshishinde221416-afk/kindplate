from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'full_name', 'email', 'role', 'is_verified', 'created_at']
    list_filter = ['role', 'is_verified', 'is_active']
    search_fields = ['username', 'email', 'full_name', 'phone_number']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {
            'fields': ('role', 'full_name', 'phone_number', 'address', 
                      'latitude', 'longitude', 'is_verified', 'verification_document')
        }),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Custom Fields', {
            'fields': ('role', 'full_name', 'phone_number')
        }),
    )
