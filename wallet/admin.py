from django.contrib import admin
from .models import Wallet, Transaction

@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ['user', 'balance', 'total_recharged', 'total_spent', 'is_active']
    list_filter = ['is_active']
    search_fields = ['user__username', 'user__full_name']
    readonly_fields = ['total_recharged', 'total_spent']

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['wallet', 'transaction_type', 'amount', 'status', 'transaction_id', 'created_at']
    list_filter = ['transaction_type', 'status', 'payment_method']
    search_fields = ['wallet__user__username', 'transaction_id']
    date_hierarchy = 'created_at'
    readonly_fields = ['balance_before', 'balance_after']
