
import streamlit as st

from modules.inventory import (
    inventory,
    load_inventory,
    add_product,
    update_product,
    delete_product
)

from modules.sales import record_sale, view_sales

from modules.reports import (
    inventory_summary,
    category_report,
    sales_summary,
    best_selling_products,
    low_stock_report
)


# --------------------------------
# PAGE CONFIGURATION
# --------------------------------

st.set_page_config(
    page_title="Inventory Management System",
    page_icon="📦",
    layout="wide"
)


# --------------------------------
# LOAD INVENTORY DATA
# --------------------------------

load_inventory()


# --------------------------------
# DASHBOARD TITLE
# --------------------------------

st.title("📦 Product Inventory Management System")

st.write(
    "Manage your products, inventory, sales and reports."
)

st.success("Dashboard connected successfully!")


# --------------------------------
# SIDEBAR NAVIGATION
# --------------------------------

st.sidebar.title("Navigation")

menu = st.sidebar.radio(
    "Select an option",
    [
        "Dashboard",
        "Inventory",
        "Sales",
        "Reports"
    ]
)


# --------------------------------
# DASHBOARD PAGE
# --------------------------------

if menu == "Dashboard":

    st.header("Dashboard Overview")

    total_products = len(inventory)

    total_quantity = sum(
        product["quantity"]
        for product in inventory.values()
    )

    total_value = sum(
        product["price"] * product["quantity"]
        for product in inventory.values()
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Products",
        total_products
    )

    col2.metric(
        "Total Stock",
        total_quantity
    )

    col3.metric(
        "Inventory Value",
        f"₹{total_value:,.2f}"
    )

    st.info("Your inventory dashboard is ready.")


# --------------------------------
# INVENTORY PAGE
# --------------------------------


# --------------------------------
# INVENTORY MANAGEMENT PAGE
# --------------------------------

elif menu == "Inventory":

    st.header("📦 Inventory Management")

    # Create five tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "View Products",
        "Add Product",
        "Update Product",
        "Delete Product",
        "Search Product"
    ])

    # --------------------------------
    # VIEW PRODUCTS
    # --------------------------------

    with tab1:

        st.subheader("All Inventory Products")

        if inventory:

            st.dataframe(
                [
                    {
                        "Product ID": product_id,
                        "Name": details["name"],
                        "Category": details["category"],
                        "Price": details["price"],
                        "Quantity": details["quantity"]
                    }
                    for product_id, details in inventory.items()
                ],
                use_container_width=True,
                hide_index=True
            )

        else:
            st.warning("No products available.")

    # --------------------------------
    # ADD PRODUCT
    # --------------------------------

    with tab2:

        st.subheader("Add a New Product")

        with st.form("add_product_form"):

            product_id = st.text_input("Product ID")
            name = st.text_input("Product Name")
            category = st.text_input("Category")

            price = st.number_input(
                "Price (Rs.)",
                min_value=0.01,
                value=100.0,
                step=100.0
            )

            quantity = st.number_input(
                "Quantity",
                min_value=0,
                value=1,
                step=1
            )

            submitted = st.form_submit_button(
                "Add Product",
                use_container_width=True
            )

            if submitted:

                product_id = product_id.strip()

                if not product_id or not name.strip() or not category.strip():
                    st.error("Please fill in all product details.")

                elif product_id in inventory:
                    st.error("This Product ID already exists.")

                else:

                    add_product(
                        product_id,
                        name.strip(),
                        category.strip(),
                        price,
                        quantity
                    )

                    st.success("Product added successfully!")
                    st.rerun()

    # --------------------------------
    # UPDATE PRODUCT
    # --------------------------------

    with tab3:

        st.subheader("Update Existing Product")

        if inventory:

            selected_id = st.selectbox(
                "Select Product",
                list(inventory.keys())
            )

            current_product = inventory[selected_id]

            with st.form("update_product_form"):

                st.write("Product:", current_product["name"])

                new_price = st.number_input(
                    "New Price (Rs.)",
                    min_value=0.01,
                    value=float(current_product["price"]),
                    step=100.0
                )

                new_quantity = st.number_input(
                    "New Quantity",
                    min_value=0,
                    value=int(current_product["quantity"]),
                    step=1
                )

                update_button = st.form_submit_button(
                    "Update Product",
                    use_container_width=True
                )

                if update_button:

                    update_product(
                        selected_id,
                        price=new_price,
                        quantity=new_quantity
                    )

                    st.success("Product updated successfully!")
                    st.rerun()

        else:
            st.warning("No products available to update.")

    # --------------------------------
    # DELETE PRODUCT
    # --------------------------------

    with tab4:

        st.subheader("Delete Product")

        if inventory:

            selected_delete_id = st.selectbox(
                "Select Product to Delete",
                list(inventory.keys()),
                key="delete_product_select"
            )

            st.warning(
                "You are about to permanently remove this product "
                "from the inventory."
            )

            confirm_delete = st.checkbox(
                "I confirm that I want to delete this product."
            )

            if st.button(
                "Delete Product",
                disabled=not confirm_delete,
                use_container_width=True
            ):

                delete_product(selected_delete_id)

                st.success("Product deleted successfully!")
                st.rerun()

        else:
            st.warning("No products available to delete.")
                # --------------------------------
    # SEARCH PRODUCT
    # --------------------------------

    with tab5:

        st.subheader("Search Product")

        search_query = st.text_input(
            "Enter Product ID, Name, or Category",
            placeholder="Example: P101, Laptop, Electronics"
        )

        if search_query.strip():

            query = search_query.strip().lower()

            search_results = {
                product_id: details
                for product_id, details in inventory.items()
                if query in product_id.lower()
                or query in details["name"].lower()
                or query in details["category"].lower()
            }

            if search_results:

                st.success(f"{len(search_results)} matching product(s) found.")

                st.dataframe(
                    [
                        {
                            "Product ID": product_id,
                            "Name": details["name"],
                            "Category": details["category"],
                            "Price": details["price"],
                            "Quantity": details["quantity"]
                        }
                        for product_id, details in search_results.items()
                    ],
                    use_container_width=True,
                    hide_index=True
                )

            else:
                st.warning("No matching product found.")

        else:
            st.info("Enter a Product ID, product name, or category to search.")

#
# --------------------------------
# SALES MANAGEMENT
# --------------------------------

elif menu == "Sales":

    st.header("💰 Sales Management")

    tab1, tab2 = st.tabs(["Record a Sale", "Sales History"])

    # RECORD A SALE
    with tab1:

        st.subheader("Record New Sale")

        if inventory:

            with st.form("record_sale_form"):

                selected_id = st.selectbox(
                    "Select Product",
                    list(inventory.keys())
                )

                product = inventory[selected_id]

                st.write("Product:", product["name"])
                st.write("Available Stock:", product["quantity"])
                st.write("Unit Price: ₹", product["price"])

                quantity_sold = st.number_input(
                    "Quantity to Sell",
                    min_value=1,
                    value=1,
                    step=1
                )

                total = product["price"] * quantity_sold

                st.metric("Total Sale Amount", f"₹{total:,.2f}")

                submitted = st.form_submit_button(
                    "Record Sale",
                    use_container_width=True
                )

                if submitted:

                    if quantity_sold > product["quantity"]:

                        st.error(
                            f"Insufficient stock! Only "
                            f"{product['quantity']} units are available."
                        )

                    else:

                        result = record_sale(selected_id, quantity_sold)

                        if result is True:
                            st.success("Sale recorded successfully!")
                            st.rerun()
                        else:
                            st.error("Sale could not be recorded.")

        else:
            st.warning("No products available.")

    # SALES HISTORY
    with tab2:

        st.subheader("Sales History")

        import pandas as pd
        import os

        sales_file = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "data",
            "sales.csv"
        )

        if os.path.exists(sales_file):

            sales_df = pd.read_csv(sales_file)

            if not sales_df.empty:

                st.dataframe(
                    sales_df,
                    use_container_width=True,
                    hide_index=True
                )

                st.success(
                    f"Total transactions: {len(sales_df)}"
                )

            else:
                st.info("No sales transactions recorded yet.")

        else:
            st.warning("Sales file not found.")


# --------------------------------
# REPORTS DASHBOARD
# --------------------------------

elif menu == "Reports":

    st.header("📊 Business Reports")

    import pandas as pd
    import os

    # INVENTORY SUMMARY
    st.subheader("Inventory Overview")

    total_products = len(inventory)

    total_stock = sum(
        item["quantity"] for item in inventory.values()
    )

    inventory_value = sum(
        item["price"] * item["quantity"]
        for item in inventory.values()
    )

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Products", total_products)
    col2.metric("Total Stock", total_stock)
    col3.metric("Inventory Value", f"₹{inventory_value:,.2f}")

    st.divider()

    # CATEGORY-WISE INVENTORY
    st.subheader("Category-wise Inventory")

    category_data = {}

    for item in inventory.values():
        category = item["category"]
        category_data[category] = (
            category_data.get(category, 0) + item["quantity"]
        )

    if category_data:
        st.bar_chart(category_data)
    else:
        st.info("No category data available.")

    st.divider()

    # LOW STOCK REPORT
    st.subheader("Low Stock Products")

    low_stock = [
        {
            "Product ID": product_id,
            "Name": details["name"],
            "Quantity": details["quantity"]
        }
        for product_id, details in inventory.items()
        if details["quantity"] <= 5
    ]

    if low_stock:
        st.dataframe(low_stock, use_container_width=True)
    else:
        st.success("No low-stock products found.")

    st.divider()

    # SALES ANALYTICS
    st.subheader("💰 Sales Analytics")

    sales_file = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "data",
        "sales.csv"
    )

    if os.path.exists(sales_file):

        sales_df = pd.read_csv(sales_file)

        if not sales_df.empty:

            sales_df["date"] = pd.to_datetime(
                sales_df["date"], errors="coerce"
            )

            sales_df["total"] = pd.to_numeric(
                sales_df["total"], errors="coerce"
            )

            sales_df["quantity_sold"] = pd.to_numeric(
                sales_df["quantity_sold"], errors="coerce"
            )

            sales_df = sales_df.dropna(
                subset=["date", "total", "quantity_sold"]
            )

            if not sales_df.empty:

                # DATE FILTER
                st.subheader("Filter Sales by Date")

                min_date = sales_df["date"].min().date()
                max_date = sales_df["date"].max().date()

                col1, col2 = st.columns(2)

                start_date = col1.date_input(
                    "Start Date",
                    value=min_date,
                    min_value=min_date,
                    max_value=max_date,
                    key="report_start_date"
                )

                end_date = col2.date_input(
                    "End Date",
                    value=max_date,
                    min_value=min_date,
                    max_value=max_date,
                    key="report_end_date"
                )

                if start_date <= end_date:

                    filtered_sales = sales_df[
                        (sales_df["date"].dt.date >= start_date) &
                        (sales_df["date"].dt.date <= end_date)
                    ].copy()

                    # CATEGORY INFORMATION
                    category_map = {
                        pid: details["category"]
                        for pid, details in inventory.items()
                    }

                    filtered_sales["category"] = (
                        filtered_sales["product_id"]
                        .map(category_map)
                        .fillna("Unknown")
                    )

                    st.subheader("Advanced Sales Filters")

                    col1, col2 = st.columns(2)

                    # PRODUCT FILTER
                    products = sorted(
                        filtered_sales["product_id"].dropna().unique().tolist()
                    )

                    selected_product = col1.selectbox(
                        "Filter by Product",
                        ["All Products"] + products
                    )

                    # CATEGORY FILTER
                    categories = sorted(
                        filtered_sales["category"].unique().tolist()
                    )

                    selected_category = col2.selectbox(
                        "Filter by Category",
                        ["All Categories"] + categories
                    )

                    sale_id_search = st.text_input(
                        "Search by Sale ID",
                        placeholder="Example: S001"
                    )

                    if not filtered_sales.empty:

                        minimum = float(filtered_sales["total"].min())
                        maximum = float(filtered_sales["total"].max())

                        revenue_min, revenue_max = st.slider(
                            "Revenue Range (₹)",
                            min_value=minimum,
                            max_value=maximum,
                            value=(minimum, maximum),
                            key="revenue_filter"
                        )

                        # APPLY FILTERS
                        if selected_product != "All Products":
                            filtered_sales = filtered_sales[
                                filtered_sales["product_id"] == selected_product
                            ]

                        if selected_category != "All Categories":
                            filtered_sales = filtered_sales[
                                filtered_sales["category"] == selected_category
                            ]

                        if sale_id_search.strip():
                            filtered_sales = filtered_sales[
                                filtered_sales["sale_id"].astype(str).str.contains(
                                    sale_id_search.strip(),
                                    case=False,
                                    na=False
                                )
                            ]

                        filtered_sales = filtered_sales[
                            (filtered_sales["total"] >= revenue_min) &
                            (filtered_sales["total"] <= revenue_max)
                        ]

                    st.caption(
                        f"Showing {len(filtered_sales)} matching transaction(s)."
                    )

                    # SUMMARY
                    col1, col2, col3 = st.columns(3)

                    col1.metric(
                        "Total Revenue",
                        f"₹{filtered_sales['total'].sum():,.2f}"
                    )

                    col2.metric(
                        "Units Sold",
                        int(filtered_sales["quantity_sold"].sum())
                    )

                    col3.metric(
                        "Total Transactions",
                        len(filtered_sales)
                    )

                    if not filtered_sales.empty:

                        st.subheader("Daily Revenue Trend")

                        daily_sales = (
                            filtered_sales.groupby(
                                filtered_sales["date"].dt.date
                            )["total"].sum()
                        )

                        st.line_chart(daily_sales)

                        st.subheader("Product-wise Revenue")

                        product_revenue = (
                            filtered_sales.groupby("product_id")["total"]
                            .sum()
                            .sort_values(ascending=False)
                        )

                        product_revenue.index = [
                            inventory[pid]["name"] if pid in inventory else pid
                            for pid in product_revenue.index
                        ]

                        st.bar_chart(product_revenue)

                        st.subheader("Best-Selling Products")

                        product_sales = (
                            filtered_sales.groupby("product_id")["quantity_sold"]
                            .sum()
                            .sort_values(ascending=False)
                        )

                        product_sales.index = [
                            inventory[pid]["name"] if pid in inventory else pid
                            for pid in product_sales.index
                        ]

                        st.bar_chart(product_sales)

                    else:
                        st.info("No transactions match the selected filters.")

                    st.subheader("Sales Transaction History")

                    st.dataframe(
                        filtered_sales,
                        use_container_width=True,
                        hide_index=True
                    )

                else:
                    st.error("Start date cannot be after end date.")

            else:
                st.info("No valid sales records available.")

        else:
            st.info("No sales transactions available.")

    else:
        st.warning("Sales file not found.")
