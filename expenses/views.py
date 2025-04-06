from rest_framework import viewsets, permissions
from .models import Expense
from .serializers import ExpenseSerializer

class ExpenseViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing expenses.
    """
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Optionally restricts the returned expenses to a given trip,
        by filtering against a `trip` query parameter in the URL.
        """
        queryset = Expense.objects.all()
        trip = self.request.query_params.get('trip', None)
        if trip is not None:
            queryset = queryset.filter(trip=trip)
        return queryset.select_related('trip')

    def perform_create(self, serializer):
        """
        Save the expense and associate it with the authenticated user's trip
        """
        serializer.save()

    def perform_update(self, serializer):
        """
        Update the expense
        """
        serializer.save()
