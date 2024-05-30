from django.contrib import admin
from .models import Bank, Category, Transaction, Statements

@admin.register(Bank)
class BankAdmin(admin.ModelAdmin):
    list_display = ('name', 'balance')
    search_fields = ('name',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'category', 'type', 'amount', 'date', 'description')
    list_filter = ('type', 'date', 'category')
    search_fields = ('user__username', 'category__name', 'description')

@admin.register(Statements)
class StatementsAdmin(admin.ModelAdmin):
    list_display = ('transaction', 'bank', 'user', 'left_balance', 'date')
    search_fields = ('transaction__amount', 'bank__name', 'user__username', 'left_balance', 'date')
    list_filter = ('date', 'bank', 'user')
