from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ExpenseViewSet

# Create a router and register our viewset
router = DefaultRouter()
router.register(r'', ExpenseViewSet, basename='expense')

# The API URLs are now determined automatically by the router
urlpatterns = [
    path('', include(router.urls)),
    path('expenses/<int:pk>/', ExpenseViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='expense-detail'),
    path('expenses/', ExpenseViewSet.as_view({'get': 'list', 'post': 'create'}), name='expense-list'),
]
