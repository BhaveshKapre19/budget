# budget/forms.py

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Transaction, Category

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class TransactionForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={'class': 'datepicker', 'type': 'date'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['type'].widget = forms.Select(choices=Transaction.TRANSACTION_TYPE)
        self.fields['mode'] = forms.ChoiceField(choices=Transaction.TRANSACTION_MODE)

    class Meta:
        model = Transaction
        fields = ['bank', 'category', 'type', 'mode', 'amount', 'description', 'date']
