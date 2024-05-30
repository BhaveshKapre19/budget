# budget/views.py
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, TemplateView, View
from .forms import UserRegisterForm, TransactionForm
from .models import Transaction , Bank
from django.contrib.auth import login as auth_login
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa


class DemoView(TemplateView):
    template_name = "budget/demo.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        transactions = Transaction.objects.all()
        context['transactions'] = transactions
        return context



class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'budget/home.html'
    login_url = '/login/'  # Customize login URL if needed

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # User Info
        context['username'] = user.username
        context['email'] = user.email
        context['banks'] = Bank.objects.all()

        # Calculate total amount spent and earned in the last 30 days
        thirty_days_ago = timezone.now() - timedelta(days=30)
        total_spent_last_30_days = Transaction.objects.filter(
            user=user,
            date__gte=thirty_days_ago,
            type='expense'
        ).aggregate(Sum('amount'))['amount__sum'] or 0

        total_income_last_30_days = Transaction.objects.filter(
            user=user,
            date__gte=thirty_days_ago,
            type='income'
        ).aggregate(Sum('amount'))['amount__sum'] or 0

        context['total_spent_last_30_days'] = total_spent_last_30_days
        context['total_income_last_30_days'] = total_income_last_30_days

        # Get recent transactions
        recent_transactions = Transaction.objects.filter(
            user=user
        ).order_by('-date')[:5]  # Get the latest 5 transactions

        context['recent_transactions'] = recent_transactions

        # Filtered Transactions
        filter_type = self.request.GET.get('filter')
        transactions = Transaction.objects.filter(user=user)
        if filter_type:
            transactions = transactions.filter(type=filter_type)
        context['transactions'] = transactions

        return context

class ExportPDFView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user = request.user
        transactions = Transaction.objects.filter(user=user)
        template_path = 'budget/export_pdf.html'
        context = {'transactions': transactions, 'user': user}
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="transactions.pdf"'
        template = get_template(template_path)
        html = template.render(context)
        pisa_status = pisa.CreatePDF(
            html, dest=response
        )
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        return response

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
        # Check if it's an expense transaction
        if form.instance.type == 'expense':
            # Get the bank balance
            bank_balance = form.instance.bank.balance

            # Get the amount of the transaction
            transaction_amount = form.cleaned_data.get('amount')

            # Check if the expense amount is greater than the bank balance
            if transaction_amount > bank_balance:
                # If the balance would become negative, show an error message
                messages.error(self.request, "Expense amount cannot be greater than bank balance.")
                return self.form_invalid(form)
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





