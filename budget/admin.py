# budget/admin.py

from django.contrib import admin
from .models import Category, Transaction

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'category', 'type', 'amount', 'date', 'description')
    list_filter = ('type', 'date', 'category')
    search_fields = ('user__username', 'category__name', 'description')
