# budget/urls.py

from django.urls import path
from .views import DemoView, ExportPDFView,HomeView, RegisterView, TransactionListView, TransactionCreateView, TransactionUpdateView, TransactionDeleteView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('register/', RegisterView.as_view(), name='register'),
    path('transactions/', TransactionListView.as_view(), name='transaction-list'),
    path('transaction/new/', TransactionCreateView.as_view(), name='transaction-create'),
    path('transaction/<int:pk>/edit/', TransactionUpdateView.as_view(), name='transaction-edit'),
    path('transaction/<int:pk>/delete/', TransactionDeleteView.as_view(), name='transaction-delete'),
    path('transactions/export_pdf/', ExportPDFView.as_view(), name='export_pdf'),
    path('transactions/demo', DemoView.as_view(), name='demo'),
]
