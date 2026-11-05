"""
StockWise - Smart Warehouse Inventory Management System
A beginner-friendly Python project using CSV for persistent storage.
Run: python main.py
"""

import csv
from datetime import datetime, date
from pathlib import Path

DATA_FILE = Path(__file__).with_name("inventory.csv")
FIELDS = ["product_id", "name", "category", "quantity", "min_stock", "expiry_date"]


def load_inventory():
    if not DATA_FILE.exists():
        with DATA_FILE.open("w", newline="", encoding="utf-8") as f:
            csv.DictWriter(f, fieldnames=FIELDS).writeheader()
        return []
    with DATA_FILE.open("r", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def save_inventory(items):
    with DATA_FILE.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(items)


def get_int(prompt, minimum=0):
    while True:
        try:
            value = int(input(prompt))
            if value < minimum:
                print(f"Enter a number greater than or equal to {minimum}.")
                continue
            return value
        except ValueError:
            print("Please enter a whole number.")


def add_product(items):
    product_id = input("Product ID: ").strip()
    if not product_id or any(p["product_id"].lower() == product_id.lower() for p in items):
        print("ID cannot be blank or already exist.")
        return
    name = input("Product name: ").strip()
    category = input("Category: ").strip()
    if not name:
        print("Product name cannot be blank.")
        return
    quantity = get_int("Opening quantity: ")
    minimum = get_int("Minimum stock level: ")
    expiry = input("Expiry date (YYYY-MM-DD, or leave blank): ").strip()
    if expiry:
        try:
            datetime.strptime(expiry, "%Y-%m-%d")
        except ValueError:
            print("Invalid date. Use YYYY-MM-DD.")
            return
    items.append({
        "product_id": product_id, "name": name, "category": category,
        "quantity": str(quantity), "min_stock": str(minimum), "expiry_date": expiry
    })
    save_inventory(items)
    print("Product added successfully.")


def list_products(items):
    if not items:
        print("Inventory is empty.")
        return
    print("\n{:<12} {:<22} {:<16} {:>9} {:>10} {:<12}".format(
        "ID", "PRODUCT", "CATEGORY", "QUANTITY", "MINIMUM", "EXPIRY"))
    print("-" * 86)
    for p in items:
        print("{:<12} {:<22} {:<16} {:>9} {:>10} {:<12}".format(
            p["product_id"], p["name"][:21], p["category"][:15],
            p["quantity"], p["min_stock"], p["expiry_date"] or "N/A"))


def find_product(items, product_id):
    return next((p for p in items if p["product_id"].lower() == product_id.lower()), None)


def change_stock(items, action):
    product_id = input("Enter product ID: ").strip()
    product = find_product(items, product_id)
    if not product:
        print("Product not found.")
        return
    amount = get_int("Quantity: ", 1)
    current = int(product["quantity"])
    if action == "out" and amount > current:
        print(f"Insufficient stock. Available quantity: {current}")
        return
    product["quantity"] = str(current + amount if action == "in" else current - amount)
    save_inventory(items)
    print("Stock updated successfully.")


def show_alerts(items):
    today = date.today()
    low = [p for p in items if int(p["quantity"]) <= int(p["min_stock"])]
    expiring = []
    expired = []
    for p in items:
        if not p["expiry_date"]:
            continue
        try:
            days = (datetime.strptime(p["expiry_date"], "%Y-%m-%d").date() - today).days
            if days < 0:
                expired.append(p)
            elif days <= 30:
                expiring.append((p, days))
        except ValueError:
            continue

    print("\n--- LOW STOCK ALERTS ---")
    if low:
        for p in low:
            print(f'{p["name"]} ({p["product_id"]}): {p["quantity"]} left; minimum is {p["min_stock"]}')
    else:
        print("No low-stock products.")

    print("\n--- EXPIRY ALERTS (NEXT 30 DAYS) ---")
    if expiring:
        for p, days in expiring:
            print(f'{p["name"]}: expires in {days} day(s) ({p["expiry_date"]})')
    else:
        print("No products expiring in the next 30 days.")

    print("\n--- EXPIRED PRODUCTS ---")
    if expired:
        for p in expired:
            print(f'{p["name"]}: expired on {p["expiry_date"]}')
    else:
        print("No expired products.")


def search_product(items):
    term = input("Search by ID or product name: ").strip().lower()
    matches = [p for p in items if term in p["product_id"].lower() or term in p["name"].lower()]
    list_products(matches)


def main():
    items = load_inventory()
    while True:
        print("\n========== STOCKWISE ==========")
        print("1. Add product")
        print("2. View all products")
        print("3. Stock received (stock in)")
        print("4. Stock dispatched (stock out)")
        print("5. Low-stock and expiry alerts")
        print("6. Search products")
        print("7. Exit")
        choice = input("Choose an option (1-7): ").strip()

        if choice == "1":
            add_product(items)
        elif choice == "2":
            list_products(items)
        elif choice == "3":
            change_stock(items, "in")
        elif choice == "4":
            change_stock(items, "out")
        elif choice == "5":
            show_alerts(items)
        elif choice == "6":
            search_product(items)
        elif choice == "7":
            print("Thank you for using StockWise!")
            break
        else:
            print("Invalid choice. Select 1 to 7.")


if __name__ == "__main__":
    main()
