from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from users.models import CustomUser

class Trip(models.Model):
    """Represents a business trip with detailed location and purpose"""
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='trips')
    purpose = models.TextField()
    description = models.TextField(blank=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    status = models.CharField(max_length=10, default='planned')
    total_expense = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['user', 'start_date'], name='trip_user_date_idx'),
            models.Index(fields=['status'], name='trip_status_idx')
        ]