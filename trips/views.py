from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Trip
from .serializers import TripSerializer

class TripListCreateView(generics.ListCreateAPIView):
    """View for listing all trips and creating new trips"""
    serializer_class = TripSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter trips by authenticated user"""
        return Trip.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Set the user to the authenticated user when creating"""
        serializer.save(user=self.request.user)

class TripDetailView(generics.RetrieveUpdateDestroyAPIView):
    """View for retrieving, updating and deleting individual trips"""
    serializer_class = TripSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter trips by authenticated user"""
        return Trip.objects.filter(user=self.request.user)

    def update(self, request, *args, **kwargs):
        """Handle partial and full updates"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """Delete a trip"""
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
