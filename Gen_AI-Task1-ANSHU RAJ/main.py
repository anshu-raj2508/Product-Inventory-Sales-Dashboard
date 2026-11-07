
# Product Inventory and Sales Management System

from modules.reports import generate_reports
from modules.inventory import (
    add_product,
    view_products,
    search_product,
    update_product,
    delete_product,
    load_inventory
)

from modules.sales import record_sale, view_sales


def main():

    # Load saved inventory when the program starts
    load_inventory()

    while True:
        print("\n========== INVENTORY MANAGEMENT SYSTEM ==========")
        print("1. Add Product")
        print("2. View All Products")
        print("3. Search Product")
        print("4. Update Product")
        print("5. Delete Product")
        print("6. Record a Sale")
        print("7. View Sales History")
        print("8. Exit")
        print("9. Generate Reports")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            product_id = input("Enter Product ID: ")
            name = input("Enter Product Name: ")
            category = input("Enter Category: ")

            try:
                price = float(input("Enter Price: "))
                quantity = int(input("Enter Quantity: "))
                add_product(product_id, name, category, price, quantity)
            except ValueError:
                print("Please enter a valid price and quantity.")

        elif choice == "2":
            view_products()

        elif choice == "3":
            product_id = input("Enter Product ID to search: ")
            search_product(product_id)

        elif choice == "4":
            product_id = input("Enter Product ID to update: ")

            try:
                price_input = input("Enter new price (press Enter to skip): ")
                quantity_input = input("Enter new quantity (press Enter to skip): ")

                price = float(price_input) if price_input else None
                quantity = int(quantity_input) if quantity_input else None

                if price is None and quantity is None:
                    print("No changes entered.")
                else:
                    update_product(product_id, price, quantity)

            except ValueError:
                print("Please enter valid numeric values.")

        elif choice == "5":
            product_id = input("Enter Product ID to delete: ")
            delete_product(product_id)

        elif choice == "6":
            product_id = input("Enter Product ID to sell: ")

            try:
                quantity = int(input("Enter quantity to sell: "))
                record_sale(product_id, quantity)
            except ValueError:
                print("Please enter a valid whole number for quantity.")

        elif choice == "7":
            view_sales()

        elif choice == "8":
            print("Thank you for using Inventory Management System!")
            break
        elif choice == "9":
            generate_reports()

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()


