
# Sales Management Module

import csv
import os
from datetime import datetime

from modules.inventory import inventory, save_inventory

# Locate sales.csv inside the data folder
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SALES_FILE = os.path.join(BASE_DIR, "data", "sales.csv")


def get_next_sale_id():
    """Generate the next sale ID."""
    os.makedirs(os.path.dirname(SALES_FILE), exist_ok=True)

    if not os.path.exists(SALES_FILE) or os.path.getsize(SALES_FILE) == 0:
        with open(SALES_FILE, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([
                "sale_id", "product_id", "quantity_sold",
                "unit_price", "total", "date"
            ])

    with open(SALES_FILE, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        sale_numbers = []

        for row in reader:
            try:
                sale_numbers.append(int(row["sale_id"].replace("S", "")))
            except (ValueError, KeyError, AttributeError):
                continue

    next_number = max(sale_numbers, default=0) + 1
    return f"S{next_number:03d}"



def record_sale(product_id, quantity_sold):
    """Record a sale and reduce available inventory stock."""

    if product_id not in inventory:
        print("Error: Product not found.")
        return False

    if quantity_sold <= 0:
        print("Error: Sale quantity must be greater than zero.")
        return False

    product = inventory[product_id]

    if quantity_sold > product["quantity"]:
        print("Error: Not enough stock available.")
        print("Available quantity:", product["quantity"])
        return False

    unit_price = product["price"]
    total = unit_price * quantity_sold

    # Create sale record
    sale_id = get_next_sale_id()
    sale_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    sale_record = {
        "sale_id": sale_id,
        "product_id": product_id,
        "quantity_sold": quantity_sold,
        "unit_price": unit_price,
        "total": total,
        "date": sale_date
    }

    # Append sale record to CSV
    with open(SALES_FILE, "a", newline="", encoding="utf-8") as file:
        fieldnames = [
            "sale_id", "product_id", "quantity_sold",
            "unit_price", "total", "date"
        ]

        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writerow(sale_record)

    # Reduce inventory quantity only after recording the sale
    product["quantity"] -= quantity_sold

    # Save updated inventory
    save_inventory()

    print("\nSale recorded successfully!")
    print("Sale ID:", sale_id)
    print("Product:", product["name"])
    print("Quantity sold:", quantity_sold)
    print("Unit price: Rs.", unit_price)
    print("Total amount: Rs.", total)
    print("Remaining stock:", product["quantity"])

    return True


def view_sales():
    """Display all saved sales records."""

    if not os.path.exists(SALES_FILE) or os.path.getsize(SALES_FILE) == 0:
        print("\nNo sales records found.")
        return

    with open(SALES_FILE, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        sales = list(reader)

    if not sales:
        print("\nNo sales records found.")
        return

    print("\n" + "-" * 90)
    print(
        f"{'Sale ID':<12}{'Product ID':<15}"
        f"{'Quantity':<12}{'Unit Price':<15}"
        f"{'Total':<15}{'Date':<20}"
    )
    print("-" * 90)

    for sale in sales:
        print(
            f"{sale['sale_id']:<12}"
            f"{sale['product_id']:<15}"
            f"{sale['quantity_sold']:<12}"
            f"{float(sale['unit_price']):<15.2f}"
            f"{float(sale['total']):<15.2f}"
            f"{sale['date']:<20}"
        )

    print("-" * 90)
