# Generated by Django 4.2.13 on 2024-05-30 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0008_delete_statement'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='remaining_balance',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
