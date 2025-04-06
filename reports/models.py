from django.db import models
from users.models import CustomUser


class WeeklyReport(models.Model):
    """Represents a weekly expense report for reimbursement"""
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='reports')
    week_start = models.DateField()
    week_end = models.DateField()
    status = models.CharField(max_length=10, default='draft')
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    report_file = models.FileField(upload_to='reports/%Y/%m/', null=True, blank=True)
    submitted_at = models.DateTimeField(null=True, blank=True)
    comments = models.TextField(blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['user', 'week_start'], name='report_user_week_idx'),
            models.Index(fields=['status'], name='report_status_idx')
        ]

