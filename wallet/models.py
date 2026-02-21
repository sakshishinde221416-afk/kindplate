from django.db import models
from django.conf import settings
from decimal import Decimal

class Wallet(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wallet')
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    total_recharged = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_spent = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'wallets'
    
    def __str__(self):
        return f"{self.user.full_name} - ₹{self.balance}"
    
    def add_balance(self, amount):
        self.balance += Decimal(str(amount))
        self.total_recharged += Decimal(str(amount))
        self.save()
    
    def deduct_balance(self, amount):
        if self.balance >= Decimal(str(amount)):
            self.balance -= Decimal(str(amount))
            self.total_spent += Decimal(str(amount))
            self.save()
            return True
        return False
    
    def has_sufficient_balance(self, amount):
        return self.balance >= Decimal(str(amount))


class Transaction(models.Model):
    TRANSACTION_TYPE_CHOICES = [
        ('recharge', 'Wallet Recharge'),
        ('delivery_payment', 'Delivery Payment'),
        ('refund', 'Refund'),
        ('bonus', 'Bonus Credit'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    transaction_id = models.CharField(max_length=100, unique=True)
    payment_method = models.CharField(max_length=50, default='demo')
    
    description = models.TextField(blank=True)
    reference_id = models.CharField(max_length=100, blank=True)
    
    balance_before = models.DecimalField(max_digits=10, decimal_places=2)
    balance_after = models.DecimalField(max_digits=10, decimal_places=2)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'wallet_transactions'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['wallet', 'status']),
            models.Index(fields=['transaction_id']),
        ]
    
    def __str__(self):
        return f"{self.wallet.user.full_name} - {self.transaction_type} - ₹{self.amount}"
