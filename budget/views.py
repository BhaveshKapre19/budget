from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic import CreateView, ListView, UpdateView, DeleteView,TemplateView
from .forms import UserRegisterForm, TransactionForm
from .models import Transaction
from django.contrib.auth import login as auth_login
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta

class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'budget/home.html'
    login_url = '/login/'  # Customize login URL if needed

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Calculate total amount spent in the last 30 days
        thirty_days_ago = timezone.now() - timedelta(days=30)
        total_spent_last_30_days = Transaction.objects.filter(
            user=self.request.user,
            date__gte=thirty_days_ago
        ).aggregate(Sum('amount'))['amount__sum'] or 0
        context['total_spent_last_30_days'] = total_spent_last_30_days
        # Get recent transactions
        recent_transactions = Transaction.objects.filter(
            user=self.request.user
        ).order_by('-date')[:5]  # Get the latest 5 transactions
        context['recent_transactions'] = recent_transactions
        return context


class RegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = 'budget/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        auth_login(self.request, user)
        return redirect('home')

class TransactionListView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = 'budget/transaction_list.html'
    context_object_name = 'transactions'
    login_url = '/login/'  # Customize login URL if needed

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

class TransactionCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = TransactionForm
    template_name = 'budget/transaction_form.html'
    success_url = reverse_lazy('transaction-list')
    success_message = "Transaction created successfully."  # Custom success message
    login_url = '/login/'  # Customize login URL if needed

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class TransactionUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'budget/transaction_form.html'
    success_url = reverse_lazy('transaction-list')
    success_message = "Transaction updated successfully."  # Custom success message
    login_url = '/login/'  # Customize login URL if needed

class TransactionDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Transaction
    template_name = 'budget/transaction_confirm_delete.html'
    success_url = reverse_lazy('transaction-list')
    success_message = "Transaction deleted successfully."  # Custom success message
    login_url = '/login/'  # Customize login URL if needed
