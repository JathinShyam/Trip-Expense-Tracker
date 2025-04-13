from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from users.models import CustomUser

class Expense(models.Model):
    """
    Model for tracking expenses submitted by users.
    """
    
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='expenses')
    category = models.TextField()
    description = models.TextField()
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    # receipt = models.FileField(upload_to='receipts/', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['category'], name='category_idx'),
        ]
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username}'s expense: {self.amount} ({self.status})"
    
    def save(self, *args, **kwargs):
        """
        Override save method to ensure updated_at is set correctly.
        """
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super(Expense, self).save(*args, **kwargs)