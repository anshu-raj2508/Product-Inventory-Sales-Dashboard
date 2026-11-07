
import csv
import os

from modules.inventory import inventory

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SALES_FILE = os.path.join(BASE_DIR, "data", "sales.csv")


def inventory_summary():
    print("\n========== INVENTORY SUMMARY ==========")

    total_products = len(inventory)
    total_quantity = sum(
        product["quantity"] for product in inventory.values()
    )
    total_value = sum(
        product["price"] * product["quantity"]
        for product in inventory.values()
    )

    print("Total Products:", total_products)
    print("Total Stock Quantity:", total_quantity)
    print(f"Total Inventory Value: Rs. {total_value:.2f}")


def category_report():
    print("\n========== CATEGORY REPORT ==========")

    categories = {}

    for product in inventory.values():
        category = product["category"]

        if category not in categories:
            categories[category] = {
                "products": 0,
                "quantity": 0
            }

        categories[category]["products"] += 1
        categories[category]["quantity"] += product["quantity"]

    if not categories:
        print("No products available.")
        return

    print(f"{'Category':<20}{'Products':<15}{'Quantity':<15}")
    print("-" * 50)

    for category, details in categories.items():
        print(
            f"{category:<20}"
            f"{details['products']:<15}"
            f"{details['quantity']:<15}"
        )


def read_sales():
    if not os.path.exists(SALES_FILE) or os.path.getsize(SALES_FILE) == 0:
        return []

    with open(SALES_FILE, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return list(reader)


def sales_summary():
    print("\n========== SALES SUMMARY ==========")

    sales = read_sales()

    if not sales:
        print("No sales records found.")
        return

    total_transactions = len(sales)
    total_units_sold = 0
    total_revenue = 0

    for sale in sales:
        total_units_sold += int(sale["quantity_sold"])
        total_revenue += float(sale["total"])

    print("Total Transactions:", total_transactions)
    print("Total Units Sold:", total_units_sold)
    print(f"Total Sales Revenue: Rs. {total_revenue:.2f}")


def best_selling_products():
    print("\n========== BEST-SELLING PRODUCTS ==========")

    sales = read_sales()
    product_sales = {}

    for sale in sales:
        product_id = sale["product_id"]
        quantity = int(sale["quantity_sold"])

        product_sales[product_id] = (
            product_sales.get(product_id, 0) + quantity
        )

    if not product_sales:
        print("No sales records found.")
        return

    print(f"{'Product ID':<15}{'Product Name':<22}{'Units Sold':<15}")
    print("-" * 52)

    sorted_products = sorted(
        product_sales.items(),
        key=lambda item: item[1],
        reverse=True
    )

    for product_id, quantity in sorted_products:
        name = inventory.get(
            product_id, {}
        ).get("name", "Product no longer in inventory")

        print(f"{product_id:<15}{name:<22}{quantity:<15}")


def low_stock_report():
    print("\n========== LOW-STOCK REPORT ==========")

    low_stock = {
        product_id: details
        for product_id, details in inventory.items()
        if details["quantity"] <= 5
    }

    if not low_stock:
        print("No low-stock products found.")
        return

    print(f"{'Product ID':<15}{'Product Name':<22}{'Quantity':<15}")
    print("-" * 52)

    for product_id, details in low_stock.items():
        print(
            f"{product_id:<15}"
            f"{details['name']:<22}"
            f"{details['quantity']:<15}"
        )


def generate_reports():
    inventory_summary()
    category_report()
    sales_summary()
    best_selling_products()
    low_stock_report()
