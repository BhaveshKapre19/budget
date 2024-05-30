from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save, pre_save, pre_delete
from django.dispatch import receiver

class Bank(models.Model):
    name = models.CharField(max_length=50)
    balance = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self) -> str:
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

    def __str__(self):
        return f"{self.user.username} - {self.type} - {self.amount} - remaining balance = {self.bank.balance}"

class Statements(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.DO_NOTHING)
    bank = models.ForeignKey(Bank, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    left_balance = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    date = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Transaction: {self.transaction.amount} - Bank balance: {self.bank.balance} - Left balance: {self.left_balance}"

@receiver(post_save, sender=Transaction)
def transaction_post_save(sender, instance, created, **kwargs):
    if created:
        if instance.type == 'expense':
            if instance.bank.balance >= instance.amount:
                if instance.mode != 'cash':
                    instance.bank.balance -= instance.amount
                    instance.bank.save()
                    Statements.objects.create(
                        transaction=instance,
                        bank=instance.bank,
                        user=instance.user,
                        left_balance=instance.bank.balance,
                        description=f"Expense of {instance.amount} from {instance.bank.name}. New balance: {instance.bank.balance}"
                    )
            else:
                raise ValidationError("Bank balance is too low for this expense.")
        elif instance.type == 'income':
            if instance.mode != 'cash':
                instance.bank.balance += instance.amount
                instance.bank.save()
                Statements.objects.create(
                    transaction=instance,
                    bank=instance.bank,
                    user=instance.user,
                    left_balance=instance.bank.balance,
                    description=f"Income of {instance.amount} to {instance.bank.name}. New balance: {instance.bank.balance}"
                )

@receiver(pre_save, sender=Transaction)
def validate_expense_amount(sender, instance, **kwargs):
    if instance.pk:
        original_transaction = Transaction.objects.get(pk=instance.pk)
        if original_transaction.type != instance.type or original_transaction.amount != instance.amount:
            if original_transaction.type == 'expense' and original_transaction.mode != 'cash':
                instance.bank.balance += original_transaction.amount
            elif original_transaction.type == 'income' and original_transaction.mode != 'cash':
                instance.bank.balance -= original_transaction.amount
        instance.bank.save()

@receiver(pre_delete, sender=Transaction)
def transaction_pre_delete(sender, instance, **kwargs):
    if instance.type == 'expense':
        if instance.mode != 'cash':
            instance.bank.balance += instance.amount
    elif instance.type == 'income':
        if instance.mode != 'cash':
            instance.bank.balance -= instance.amount
    instance.bank.save()
