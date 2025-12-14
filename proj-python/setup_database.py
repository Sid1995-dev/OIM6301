"""
Database Setup Script
This script creates a SQLite database and imports CSV data.

Completed implementation:
1. Creates database tables with proper schema
2. Imports CSV files
3. Verifies data was loaded correctly
"""

import sqlite3
import csv
import os


def create_database(db_path):
    """Create SQLite database and tables.

    Args:
        db_path (str): Path to the database file

    Creates three tables:
    - customers: Customer information with primary key
    - products: Product catalog with pricing information
    - orders: Order transactions with foreign keys to customers and products
    """
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()

        # Enable foreign key support
        cursor.execute("PRAGMA foreign_keys = ON;")

        # Create customers table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS customers (
                customer_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                city TEXT NOT NULL,
                join_date TEXT NOT NULL
            )
        ''')

        # Create products table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                product_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                price REAL NOT NULL CHECK(price > 0),
                cost REAL NOT NULL CHECK(cost > 0)
            )
        ''')

        # Create orders table with foreign key constraints
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                order_id INTEGER PRIMARY KEY,
                customer_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL CHECK(quantity > 0),
                order_date TEXT NOT NULL,
                FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
                FOREIGN KEY (product_id) REFERENCES products(product_id)
            )
        ''')

        conn.commit()

    print(f"Database created: {db_path}")


def import_csv(db_path, csv_file, table_name, skip_header=True):
    """Import CSV file into database table.

    Args:
        db_path (str): Path to the database file
        csv_file (str): Path to the CSV file
        table_name (str): Name of the table to import into
        skip_header (bool): Whether to skip the first row (header)
    """
    if not os.path.exists(csv_file):
        print(f"Error: File not found: {csv_file}")
        return

    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()

        # Open CSV file and read data
        with open(csv_file, 'r', encoding='utf-8') as f:
            csv_reader = csv.reader(f)

            # Skip header row if needed
            if skip_header:
                next(csv_reader)

            # Convert to list to get data
            data = list(csv_reader)

            # Determine number of columns
            if data:
                num_cols = len(data[0])
                placeholders = ', '.join(['?'] * num_cols)

                # Import data using executemany with parameterized query
                cursor.executemany(
                    f"INSERT INTO {table_name} VALUES ({placeholders})",
                    data
                )

        conn.commit()

    print(f"Imported {csv_file} into {table_name} ({len(data)} rows)")


def verify_data(db_path):
    """Verify data was imported correctly by printing row counts.

    Args:
        db_path (str): Path to the database file
    """
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()

        print("\n=== Database Verification ===")

        # Get row count for customers
        customers_count = cursor.execute(
            "SELECT COUNT(*) FROM customers"
        ).fetchone()[0]
        print(f"Customers table: {customers_count} rows")

        # Get row count for products
        products_count = cursor.execute(
            "SELECT COUNT(*) FROM products"
        ).fetchone()[0]
        print(f"Products table: {products_count} rows")

        # Get row count for orders
        orders_count = cursor.execute(
            "SELECT COUNT(*) FROM orders"
        ).fetchone()[0]
        print(f"Orders table: {orders_count} rows")

        # Show sample data from customers table
        print("\nSample data from customers table (first 5 rows):")
        sample_customers = cursor.execute(
            "SELECT * FROM customers LIMIT 5"
        ).fetchall()

        print(f"{'ID':<5} {'Name':<20} {'Email':<25} {'City':<15} {'Join Date':<12}")
        print("-" * 80)
        for row in sample_customers:
            print(f"{row[0]:<5} {row[1]:<20} {row[2]:<25} {row[3]:<15} {row[4]:<12}")

        print("\nDatabase verification complete!")


def main():
    """Main function to set up the database."""
    # Database path
    DB_PATH = "data/myproject.db"

    # Create database and tables
    create_database(DB_PATH)

    # Import each CSV file
    import_csv(DB_PATH, "data/customers.csv", "customers")
    import_csv(DB_PATH, "data/products.csv", "products")
    import_csv(DB_PATH, "data/orders.csv", "orders")

    # Verify data
    verify_data(DB_PATH)


if __name__ == "__main__":
    main()
