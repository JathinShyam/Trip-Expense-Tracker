from rest_framework import viewsets, permissions, filters, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Expense
from .serializers import ExpenseSerializer
import logging

# Configure logger
logger = logging.getLogger(__name__)

class ExpenseViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing expense instances.
    """
    serializer_class = ExpenseSerializer
    # permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category']
    search_fields = ['description', 'category']
    ordering_fields = ['created_at', 'amount', 'category']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """
        This view should return a list of all expenses
        for the currently authenticated user.
        """
        # user = self.request.user
        # Log the query for debugging purposes
        # logger.info(f"User {user.username} accessing expenses")
        # return Expense.objects.filter(user=user)
        return Expense.objects.all()
    
    def perform_create(self, serializer):
        """
        Save the expense with the authenticated user.
        """
        # Log the create action
        # logger.info(f"User {self.request.user.username} creating new expense")
        # serializer.save(user=self.request.user)
        serializer.save()
    
    def create(self, request, *args, **kwargs):
        """
        Override create method to handle custom validation and logging.
        """
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            # Additional validation can be added here
            # For example, check if amount is positive
            if float(serializer.validated_data.get('amount', 0)) <= 0:
                return Response(
                    {"detail": "Amount must be positive."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            
            # Log success
            logger.info(f"Expense created successfully: {serializer.data['id']}")
            
            return Response(
                serializer.data, 
                status=status.HTTP_201_CREATED, 
                headers=headers
            )
        
        # Log validation errors
        logger.warning(f"Expense creation failed with errors: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def list(self, request, *args, **kwargs):
        """
        Override list method to add custom filtering and metadata.
        """
        # Optional: Add date range filtering
        start_date = request.query_params.get('start_date', None)
        end_date = request.query_params.get('end_date', None)
        
        queryset = self.get_queryset()
        
        if start_date:
            queryset = queryset.filter(created_at__gte=start_date)
        
        if end_date:
            queryset = queryset.filter(created_at__lte=end_date)
        
        # Apply filters from filter backends
        queryset = self.filter_queryset(queryset)
        
        # Calculate total amount if requested
        include_total = request.query_params.get('include_total', 'false').lower() == 'true'
        total_amount = None
        if include_total:
            total_amount = sum(expense.amount for expense in queryset)
        
        # Paginate the results
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            response = self.get_paginated_response(serializer.data)
            if include_total:
                response.data['total_amount'] = total_amount
            return response
        
        serializer = self.get_serializer(queryset, many=True)
        response_data = {
            'results': serializer.data
        }
        
        if include_total:
            response_data['total_amount'] = total_amount
        
        return Response(response_data)
    
    def update(self, request, *args, **kwargs):
        """
        Override update method for logging and validation.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        
        if serializer.is_valid():
            # Additional validation here
            if 'amount' in serializer.validated_data and float(serializer.validated_data['amount']) <= 0:
                return Response(
                    {"detail": "Amount must be positive."},
                    status=status.HTTP_400_BAD_REQUEST
                )
                
            self.perform_update(serializer)
            
            # Log update
            logger.info(f"Expense {instance.id} updated by {request.user.username}")
            
            if getattr(instance, '_prefetched_objects_cache', None):
                # If 'prefetch_related' has been applied to a queryset, we need to
                # forcibly invalidate the prefetch cache on the instance.
                instance._prefetched_objects_cache = {}
                
            return Response(serializer.data)
            
        logger.warning(f"Expense update failed with errors: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def destroy(self, request, *args, **kwargs):
        """
        Override destroy method for logging.
        """
        instance = self.get_object()
        expense_id = instance.id
        
        self.perform_destroy(instance)
        
        # Log deletion
        logger.info(f"Expense {expense_id} deleted by {request.user.username}")
        
        return Response(status=status.HTTP_204_NO_CONTENT)