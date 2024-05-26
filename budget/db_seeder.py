from budget.models import Category

# List of category names
category_names = [
    "Groceries",
    "Rent",
    "Utilities",
    "Vehical",
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

# Loop through the category names and create Category objects
for name in category_names:  # Adjust the range if you want to create fewer or more categories
    Category.objects.create(name=name)

# If you want to create more categories, uncomment the lines below
# for name in category_names[10:]:
#     Category.objects.create(name=name)

print("Categories created successfully!")
