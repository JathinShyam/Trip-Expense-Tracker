from django.db import models
from trips.models import Trip

class Expense(models.Model):
    """Represents an individual expense entry for a trip"""

    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='expenses')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=15)
    expense_details = models.JSONField(default=dict, null=True, blank=True)
    date = models.DateField()
    comments = models.TextField(blank=True)
    receipt = models.FileField(upload_to='receipts/%Y/%m/%d/', null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['trip', 'category'], name='expense_trip_category_idx'),
            models.Index(fields=['date'], name='expense_date_idx')
        ]

