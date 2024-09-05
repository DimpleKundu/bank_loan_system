from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LoanViewSet, PaymentViewSet, LedgerViewSet, AccountOverviewViewSet, CustomerViewSet

router = DefaultRouter()
router.register(r'loans', LoanViewSet, basename='loan')
router.register(r'payments', PaymentViewSet, basename='payment')
router.register(r'customers', CustomerViewSet, basename='customer')  # Add this line for customers

# Manually specify the basename for viewsets without a queryset
router.register(r'ledger', LedgerViewSet, basename='ledger')
router.register(r'account-overview', AccountOverviewViewSet, basename='account-overview')

urlpatterns = [
    path('', include(router.urls)),
    path('ledger/<int:loan_id>/', LedgerViewSet.as_view({'get': 'list'}), name='ledger'),
    path('account-overview/<int:customer_id>/', AccountOverviewViewSet.as_view({'get': 'list'}), name='account-overview'),
]
