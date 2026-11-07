# ==========================================
# GenAI Task - Product Inventory Assignment
# ==========================================


# ==========================================
# TASK 1 - Lists and Tuples
# ==========================================

# Create a list containing at least 6 products
products = [
    "Laptop",
    "Mouse",
    "Keyboard",
    "Monitor",
    "Headphones",
    "Printer"
]

# Create a sample product tuple
sample_product = ("Laptop", 75000, "Electronics")

# Print the second and last product
print("Second product:", products[1])
print("Last product:", products[-1])

# Add two new products
products.append("Webcam")
products.append("Tablet")


# ==========================================
# TASK 2 - Sets
# ==========================================

# Create a set of product categories
categories_set = {
    "Electronics",
    "Food",
    "Education"
}

# Add a new category
categories_set.add("Clothing")

# Try adding a duplicate category
# Sets automatically ignore duplicate values
categories_set.add("Electronics")

# Check whether a category exists
if "Electronics" in categories_set:
    print("Electronics category exists.")
else:
    print("Electronics category does not exist.")


# ==========================================
# TASK 3 - Dictionaries
# ==========================================

# Create a dictionary containing product prices
price_dict = {
    "Laptop": 75000,
    "Mouse": 500,
    "Keyboard": 1200,
    "Monitor": 15000,
    "Headphones": 2000,
    "Printer": 12000
}

# Add a new product
price_dict["Webcam"] = 2500

# Update the price of an existing product
price_dict["Laptop"] = 80000

# Remove a product
price_dict.pop("Mouse")

# Handle a product that does not exist
if "Camera" in price_dict:
    price_dict.pop("Camera")
    print("Camera removed.")
else:
    print("Camera not found.")

# Calculate average price
total_price = sum(price_dict.values())
average_price = total_price / len(price_dict)

print("Average price:", average_price)

# Find the most expensive product
max_product = max(price_dict, key=price_dict.get)

print("Most expensive product:", max_product)
print("Price:", price_dict[max_product])

# Find the cheapest product
min_product = min(price_dict, key=price_dict.get)

print("Cheapest product:", min_product)
print("Price:", price_dict[min_product])


# ==========================================
# TASK 4 - Catalog and Category Mapping
# ==========================================

# Create a catalog as a list of tuples
catalog = [
    ("Laptop", 80000, "Electronics"),
    ("Mouse", 500, "Electronics"),
    ("Keyboard", 1200, "Electronics"),
    ("Monitor", 15000, "Electronics"),
    ("Headphones", 2000, "Electronics"),
    ("Printer", 12000, "Electronics"),
    ("Webcam", 2500, "Electronics"),
    ("Bread", 50, "Food"),
    ("Notebook", 100, "Education")
]

# Create a dictionary mapping categories to products
category_to_products = {}

for product in catalog:
    name = product[0]
    category = product[2]

    if category not in category_to_products:
        category_to_products[category] = []

    category_to_products[category].append(name)

# Find the category with the maximum number of products
max_category = max(
    category_to_products,
    key=lambda category: len(category_to_products[category])
)

print("Category with maximum products:", max_category)
print(
    "Number of products:",
    len(category_to_products[max_category])
)