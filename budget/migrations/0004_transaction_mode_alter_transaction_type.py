# Generated by Django 4.2.13 on 2024-05-26 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0003_bank_alter_transaction_type_transaction_bank'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='mode',
            field=models.CharField(choices=[('cash', 'Cash'), ('upi', 'UPI')], default=2, max_length=7),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='transaction',
            name='type',
            field=models.CharField(choices=[('income', 'Income'), ('expense', 'Expense')], max_length=7),
        ),
    ]
