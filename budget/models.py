from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_delete , pre_save
from django.dispatch import receiver
from django.forms import ValidationError

class Bank(models.Model):
    name = models.CharField(max_length=50)
    balance = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name} - {self.balance}"

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Transaction(models.Model):
    TRANSACTION_TYPE = (
        ('income', 'Income'),
        ('expense', 'Expense'),
    )

    TRANSACTION_MODE = (
        ('cash', "Cash"),
        ('upi', "UPI")
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    type = models.CharField(max_length=7, choices=TRANSACTION_TYPE)
    mode = models.CharField(max_length=7, choices=TRANSACTION_MODE, default=TRANSACTION_MODE[0])
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField()
    description = models.TextField(blank=True, null=True)
    remaining_balance = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.type} - {self.amount} - remaining balance = {self.remaining_balance}"

@receiver(pre_save, sender=Transaction)
def check_balance_before_save(sender, instance, **kwargs):
    if instance.bank.balance < instance.amount:
        raise ValidationError("Insufficient balance.")
    if instance.type == "expense" and instance.mode != 'cash':
        instance.remaining_balance = instance.bank.balance - instance.amount
    if instance.type == "income" and instance.mode != "cash":
        instance.remaining_balance = instance.bank.balance + instance.amount

@receiver(post_save, sender=Transaction)
def update_balance_on_save(sender, instance, created, **kwargs):
    if created: 
        original_transaction = Transaction.objects.get(pk=instance.pk)
        if original_transaction.type != instance.type or original_transaction.amount != instance.amount:
            if original_transaction.type == 'expense' and original_transaction.mode != 'cash':
                original_transaction.bank.balance += original_transaction.amount
            elif original_transaction.type == 'income' and original_transaction.mode != 'cash':
                original_transaction.bank.balance -= original_transaction.amount
            original_transaction.bank.save()
        else:
            if instance.type == "expense" and instance.mode != 'cash':
                instance.bank.balance -= instance.amount
            if instance.type == "income" and instance.mode != "cash":
                instance.bank.balance += instance.amount
            
            instance.bank.save()



@receiver(pre_delete, sender=Transaction)
def update_balance_on_delete(sender, instance, **kwargs):
    if instance.mode != 'cash':  # Exclude cash transactions
        if instance.type == 'expense':
            instance.bank.balance += instance.amount  # Reverse the expense
        elif instance.type == 'income':
            instance.bank.balance -= instance.amount  # Reverse the income
        instance.bank.save()
    instance.remaining_balance = instance.bank.balance  # Update remaining balance
