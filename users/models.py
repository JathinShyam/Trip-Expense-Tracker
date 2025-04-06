from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    """Extended user model with additional fields for travel expense management"""
    department = models.CharField(max_length=20)  # Choices handled in serializer
    mobile = models.CharField(max_length=15)
    manager = models.ForeignKey(
        'self', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='team_members'
    )
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    # profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    employee_id = models.CharField(max_length=50, unique=True)

    # Add related_name to avoid clashes with auth.User
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True,
        verbose_name='groups',
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.',
    )

    class Meta:
        indexes = [
            models.Index(fields=['department', 'manager'], name='dept_manager_idx'),
            models.Index(fields=['employee_id'], name='employee_id_idx')
        ]
        ordering = ['-date_joined']
        verbose_name = 'User'
        verbose_name_plural = 'Users'
