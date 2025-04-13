from rest_framework import serializers
from .models import Expense
from decimal import Decimal
from django.db import models
from users.models import CustomUser
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
    description = serializers.CharField(required=False)
    user = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(),
        required=False,
        allow_null=True
    )
    
    class Meta:
        model = Expense
        fields = ['id', 'user', 'category', 'description', 'amount', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def create(self, validated_data):
        # Get the user from the request context
        # validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Update the instance with the validated data
        instance.category = validated_data.get('category', instance.category)
        instance.description = validated_data.get('description', instance.description)
        instance.amount = validated_data.get('amount', instance.amount)
        instance.save()
        return instance