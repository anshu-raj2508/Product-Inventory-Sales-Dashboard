
# Inventory Management Module

import csv
import os

# Find the project folder and CSV file
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(BASE_DIR, "data", "inventory.csv")

# Temporary working inventory
inventory = {}


def save_inventory():
    """Save all inventory records to the CSV file."""
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)

    with open(DATA_FILE, "w", newline="", encoding="utf-8") as file:
        fieldnames = ["product_id", "name", "category", "price", "quantity"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()

        for product_id, details in inventory.items():
            writer.writerow({
                "product_id": product_id,
                "name": details["name"],
                "category": details["category"],
                "price": details["price"],
                "quantity": details["quantity"]
            })


def load_inventory():
    """Load saved inventory records when the program starts."""
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)

    if not os.path.exists(DATA_FILE) or os.path.getsize(DATA_FILE) == 0:
        save_inventory()
        return

    inventory.clear()

    with open(DATA_FILE, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            try:
                product_id = row["product_id"]
                inventory[product_id] = {
                    "name": row["name"],
                    "category": row["category"],
                    "price": float(row["price"]),
                    "quantity": int(row["quantity"])
                }
            except (ValueError, KeyError, TypeError):
                print("Warning: A CSV record could not be loaded.")


def add_product(product_id, name, category, price, quantity):
    if product_id in inventory:
        print("Error: Product ID already exists.")
        return

    if not name.strip() or not category.strip():
        print("Error: Name and category cannot be empty.")
        return

    if price <= 0 or quantity < 0:
        print("Error: Price must be positive and quantity cannot be negative.")
        return

    inventory[product_id] = {
        "name": name,
        "category": category,
        "price": price,
        "quantity": quantity
    }

    save_inventory()
    print("Product added and saved successfully!")


def view_products():
    if not inventory:
        print("\nInventory is empty.")
        return

    print("\n" + "-" * 80)
    print(f"{'ID':<12}{'Name':<20}{'Category':<18}{'Price':<15}{'Quantity':<10}")
    print("-" * 80)

    for product_id, details in inventory.items():
        print(
            f"{product_id:<12}"
            f"{details['name']:<20}"
            f"{details['category']:<18}"
            f"{details['price']:<15.2f}"
            f"{details['quantity']:<10}"
        )

    print("-" * 80)


def search_product(product_id):
    if product_id in inventory:
        print("\nProduct found:")
        print("ID:", product_id)

        for key, value in inventory[product_id].items():
            print(f"{key.title()}: {value}")
    else:
        print("Product not found.")


def update_product(product_id, price=None, quantity=None):
    if product_id not in inventory:
        print("Product not found.")
        return

    if price is not None and price <= 0:
        print("Price must be positive.")
        return

    if quantity is not None and quantity < 0:
        print("Quantity cannot be negative.")
        return

    if price is not None:
        inventory[product_id]["price"] = price

    if quantity is not None:
        inventory[product_id]["quantity"] = quantity

    save_inventory()
    print("Product updated and saved successfully!")


def delete_product(product_id):
    if product_id in inventory:
        del inventory[product_id]
        save_inventory()
        print("Product deleted successfully!")
    else:
        print("Product not found.")


