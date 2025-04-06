from rest_framework import serializers
from .models import WeeklyReport

REPORT_STATUS_CHOICES = [
    ('draft', 'Draft'),
    ('submitted', 'Submitted'), 
    ('approved', 'Approved'),
    ('rejected', 'Rejected')
]

class WeeklyReportSerializer(serializers.ModelSerializer):
    status = serializers.ChoiceField(choices=REPORT_STATUS_CHOICES)

    class Meta:
        model = WeeklyReport
        fields = ['id', 'user', 'week_start', 'week_end', 'status', 
                 'total_amount', 'report_file', 'submitted_at', 'comments']
