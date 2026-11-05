# StockWise - Smart Warehouse Inventory Management System

## Problem statement
Warehouses need a simple way to track available products, monitor stock movement, and identify low-stock or near-expiry items. Manual tracking can lead to stockouts, excess inventory, and avoidable wastage.

## Solution
StockWise is a Python command-line application that stores inventory in a CSV file and helps warehouse staff manage products and stock movement.

## Features
- Add products with unique IDs, categories, quantities, minimum stock levels and optional expiry dates.
- View and search inventory.
- Record stock received and stock dispatched.
- Alert when stock reaches or falls below its minimum level.
- Flag products expiring within 30 days and products already expired.
- Save data locally in `inventory.csv`.

## Technology
- Python 3
- CSV file storage
- Python standard library (`csv`, `datetime`, `pathlib`)

## How to run
1. Install Python 3.
2. Download or clone this repository.
3. Open a terminal in the project folder.
4. Run:

   ```bash
   python main.py
   ```

No third-party packages are required.

## Example workflow
1. Select **1** to add a product.
2. Select **3** when new stock arrives.
3. Select **4** when stock is dispatched.
4. Select **5** to review low-stock and expiry alerts.

## Project scope and future improvements
This is a lightweight prototype for a small warehouse. Future versions could include a graphical dashboard, barcode scanning, user login, database integration, supplier purchase orders and multi-warehouse support.

## Author
Add your name and academic details here before submission.
