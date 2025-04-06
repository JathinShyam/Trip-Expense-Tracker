from rest_framework import viewsets, permissions
from .models import WeeklyReport
from .serializers import WeeklyReportSerializer
from django.utils import timezone

class WeeklyReportViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing weekly expense reports.
    """
    queryset = WeeklyReport.objects.all()
    serializer_class = WeeklyReportSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Restricts reports to those belonging to the authenticated user
        """
        return WeeklyReport.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """
        Save the report and associate it with the authenticated user
        """
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        """
        Update the report and set submitted_at if status changes to submitted
        """
        instance = self.get_object()
        if instance.status != 'submitted' and serializer.validated_data.get('status') == 'submitted':
            serializer.save(submitted_at=timezone.now())
        else:
            serializer.save()
