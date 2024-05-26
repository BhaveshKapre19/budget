# budget/models.py

from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save , pre_save
from django.dispatch import receiver


class Bank(models.Model):
    name = models.CharField(max_length=50)
    balance = models.DecimalField(max_digits=10,decimal_places=2)

    def __str__(self) -> str:
        return self.name +" - "+ str(self.balance)

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
        ('cash',"Cash"),
        ('upi',"UPI")
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE,blank=True,null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    type = models.CharField(max_length=7, choices=TRANSACTION_TYPE)
    mode = models.CharField(max_length=7, choices=TRANSACTION_MODE,default=TRANSACTION_MODE[0])
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField()
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.type} - {self.amount} - bal remaning = {self.bank.balance}"



@receiver(post_save, sender=Transaction)
def transaction_post_save(sender, instance, created, **kwargs):
    """
    A post-save signal handler for the Transaction model.
    """
    if created:
        # Check if the transaction type is expense
        if instance.type == 'expense':
            if instance.bank.balance > 100:
                if instance.mode != 'cash':
                    instance.bank.balance -= instance.amount  # Deduct the amount from the bank balance
                    print(instance.bank.balance)
            else:
                raise ValidationError("The Bank Balance is Very Low")
        elif instance.type == 'income':
            if instance.mode != 'cash':
                instance.bank.balance += instance.amount  # Add the amount to the bank balance
                print(instance.bank.balance)
        # Save the updated bank balance
        instance.bank.save()
        print(instance)


@receiver(pre_save, sender=Transaction)
def validate_expense_amount(sender, instance, **kwargs):
    if instance.type == 'expense':
        if instance.mode != 'cash':
            if instance.amount > instance.bank.balance:
                raise ValidationError("Expense amount cannot be greater than bank balance.")