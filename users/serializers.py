from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.validators import RegexValidator
from .models import CustomUser

DEPARTMENT_CHOICES = [
    ('HR', 'Human Resources'),
    ('IT', 'Information Technology'),
    ('FIN', 'Finance'), 
    ('MKT', 'Marketing'),
    ('OPS', 'Operations')
]

class CustomUserSerializer(serializers.ModelSerializer):
    """Serializer for CustomUser model with password validation"""
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True, required=True)
    department = serializers.ChoiceField(choices=DEPARTMENT_CHOICES, required=True)
    mobile = serializers.CharField(max_length=15, required=True)
    manager = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(),
        required=False,
        allow_null=True
    )

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'password', 'confirm_password', 'email',
                 'first_name', 'last_name', 'department', 'mobile', 'manager',
                 'is_active', 'date_joined', 'last_modified', 'profile_image',
                 'employee_id')
        read_only_fields = ('id', 'date_joined', 'last_modified')
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True},
            'department': {'required': True},
            'mobile': {'required': True},
            'employee_id': {'required': True}
        }

    def validate_mobile(self, value):
        """Validate mobile number format"""
        if not value.isdigit() or len(value) != 10:
            raise serializers.ValidationError("Mobile number must be exactly 10 digits.")
        return value

    def validate_manager(self, value):
        """Validate manager is not self"""
        if value and value == self.context.get('request').user:
            raise serializers.ValidationError("User cannot be their own manager")
        return value

    def validate_department(self, value):
        """Validate department is one of allowed choices"""
        if value not in dict(DEPARTMENT_CHOICES).keys():
            raise serializers.ValidationError(f"Department must be one of: {', '.join(dict(DEPARTMENT_CHOICES).keys())}")
        return value

    def validate(self, attrs):
        """Validate password match and unique email"""
        if attrs.get('password') != attrs.get('confirm_password'):
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        """Create new user with encrypted password"""
        validated_data.pop('confirm_password')
        user = CustomUser.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        """Update user, handling password separately if provided"""
        if 'password' in validated_data:
            password = validated_data.pop('password')
            confirm_password = validated_data.pop('confirm_password', None)
            instance.set_password(password)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance

class CustomUserListSerializer(serializers.ModelSerializer):
    """Simplified serializer for listing users"""
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'first_name', 'last_name',
                 'department', 'employee_id', 'is_active')
        read_only_fields = fields
