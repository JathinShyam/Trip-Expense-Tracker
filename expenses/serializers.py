from rest_framework import serializers
from .models import Expense
from trips.models import Trip
from decimal import Decimal
from django.db import models

# TODO: Implement JWT Authentication
# TODO: Implement report generation cron job
# TODO: Implement logger


CATEGORY_CHOICES = [
    ('transport', 'Transport'),
    ('food', 'Food'), 
    ('accommodation', 'Accommodation'),
    ('misc', 'Miscellaneous')
]

class ExpenseSerializer(serializers.ModelSerializer):
    category = serializers.ChoiceField(choices=CATEGORY_CHOICES)
    
    class Meta:
        model = Expense
        fields = ['id', 'trip', 'amount', 'category', 'expense_details',
                 'date', 'comments', 'receipt', 'is_verified', 'created_at']

    def create(self, validated_data):
        expense = super().create(validated_data)
        trip = expense.trip
        trip.total_expense = trip.expenses.aggregate(
            total=models.Sum('amount'))['total'] or Decimal('0.00')
        trip.save()
        return expense

    def update(self, instance, validated_data):
        old_amount = instance.amount
        expense = super().update(instance, validated_data)
        if old_amount != expense.amount:
            trip = expense.trip
            trip.total_expense = trip.expenses.aggregate(
                total=models.Sum('amount'))['total'] or Decimal('0.00')
            trip.save()
        return expense