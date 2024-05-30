from django.core.management.base import BaseCommand
from budget.models import Category

class Command(BaseCommand):
    help = 'Seed the database with categories'

    def handle(self, *args, **kwargs):
        category_names = [
            "Groceries",
            "Rent",
            "Utilities",
            "Vehicle",
            "Entertainment",
            "Healthcare",
            "Education",
            "Clothing",
            "Travel",
            "FOOD",
            "Mobile",
            "Recharges",
            "Bank-In"
        ]

        for name in category_names:
            Category.objects.get_or_create(name=name)

        self.stdout.write(self.style.SUCCESS('Categories created successfully!'))
