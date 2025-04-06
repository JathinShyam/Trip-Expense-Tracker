from rest_framework import serializers
from django.utils import timezone
from .models import Trip
from users.models import CustomUser
from users.serializers import CustomUserListSerializer

TRIP_PURPOSE_CHOICES = [
    ('MEETING', 'Client Meeting'),
    ('CONFERENCE', 'Conference/Event'),
    ('TRAINING', 'Training/Workshop'),
    ('AUDIT', 'Site Audit'),
    ('SALES', 'Sales Visit'),
    ('OTHER', 'Other Business Purpose')
]

TRIP_STATUS_CHOICES = [
    ('planned', 'Planned'),
    ('ongoing', 'Ongoing'), 
    ('completed', 'Completed'),
    ('cancelled', 'Cancelled')
]

class TripSerializer(serializers.ModelSerializer):
    """Serializer for Trip model with user details"""
    user = CustomUserListSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        source='user',
        queryset=CustomUser.objects.all(),
        write_only=True
    )
    purpose = serializers.ChoiceField(choices=TRIP_PURPOSE_CHOICES)
    status = serializers.ChoiceField(choices=TRIP_STATUS_CHOICES, default='planned')
    description = serializers.CharField(required=False, allow_blank=True)
    start_date = serializers.DateTimeField(required=True)
    end_date = serializers.DateTimeField(required=True)
    total_expense = serializers.DecimalField(
        max_digits=12, 
        decimal_places=2,
        default=0.00,
        min_value=0
    )
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Trip
        fields = ('id', 'user', 'user_id', 'purpose', 'description', 
                 'start_date', 'end_date', 'status', 'total_expense',
                 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')

    def validate(self, attrs):
        """Validate trip dates are valid"""
        if attrs.get('start_date') and attrs.get('end_date'):
            if attrs['start_date'] > attrs['end_date']:
                raise serializers.ValidationError(
                    {"end_date": "End date must be after start date"}
                )
            # if attrs['start_date'] < timezone.now():
            #     raise serializers.ValidationError(
            #         {"start_date": "Start date cannot be in the past"}
            #     )
        return attrs

    def validate_status(self, value):
        """Validate status is one of allowed values"""
        allowed_statuses = dict(TRIP_STATUS_CHOICES).keys()
        if value not in allowed_statuses:
            raise serializers.ValidationError(
                f"Status must be one of: {', '.join(allowed_statuses)}"
            )
        return value

    def validate_purpose(self, value):
        """Validate purpose is one of allowed values"""
        allowed_purposes = dict(TRIP_PURPOSE_CHOICES).keys()
        if value not in allowed_purposes:
            raise serializers.ValidationError(
                f"Purpose must be one of: {', '.join(allowed_purposes)}"
            )
        return value

