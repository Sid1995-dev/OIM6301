"""
Report Generation Script
This script generates reports and exports data from the database.

Demonstrates file I/O operations:
- Reading from database and writing to CSV
- Generating formatted text reports
"""

import sqlite3
import csv
from datetime import datetime
import os


def export_to_csv(data, filename, headers):
    """Export query results to CSV file.

    Args:
        data (list): List of tuples containing data
        filename (str): Output CSV filename
        headers (list): Column headers
    """
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(data)

    print(f"✓ Data exported to {filename} ({len(data)} rows)")


def get_top_products(db_path, limit=10):
    """Get top products by revenue.

    Args:
        db_path (str): Path to database
        limit (int): Number of top products

    Returns:
        list: List of tuples (product_name, category, units_sold, total_revenue)
    """
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        results = cursor.execute('''
            SELECT
                p.name,
                p.category,
                SUM(o.quantity) AS units_sold,
                SUM(o.quantity * p.price) AS total_revenue
            FROM products p
            JOIN orders o ON p.product_id = o.product_id
            GROUP BY p.product_id, p.name, p.category
            ORDER BY total_revenue DESC
            LIMIT ?
        ''', (limit,)).fetchall()

    return results


def generate_summary_report(db_path, output_file="report.txt"):
    """Generate a text-based summary report with key business metrics.

    Args:
        db_path (str): Path to database
        output_file (str): Output file path
    """
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()

        # 1. Total revenue
        total_revenue = cursor.execute('''
            SELECT SUM(o.quantity * p.price)
            FROM orders o
            JOIN products p ON o.product_id = p.product_id
        ''').fetchone()[0]

        # 2. Total orders
        total_orders = cursor.execute(
            'SELECT COUNT(*) FROM orders'
        ).fetchone()[0]

        # 3. Total customers
        total_customers = cursor.execute(
            'SELECT COUNT(*) FROM customers'
        ).fetchone()[0]

        # 4. Average order value
        avg_order_value = total_revenue / total_orders if total_orders > 0 else 0

        # 5. Best selling category by revenue
        best_category = cursor.execute('''
            SELECT
                p.category,
                SUM(o.quantity * p.price) AS revenue
            FROM orders o
            JOIN products p ON o.product_id = p.product_id
            GROUP BY p.category
            ORDER BY revenue DESC
            LIMIT 1
        ''').fetchone()

        # 6. Most valuable customer
        top_customer = cursor.execute('''
            SELECT
                c.name,
                SUM(o.quantity * p.price) AS total_spent
            FROM customers c
            JOIN orders o ON c.customer_id = o.customer_id
            JOIN products p ON o.product_id = p.product_id
            GROUP BY c.customer_id, c.name
            ORDER BY total_spent DESC
            LIMIT 1
        ''').fetchone()

    # Write to text file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("=" * 60 + "\n")
        f.write("E-COMMERCE BUSINESS SUMMARY REPORT\n")
        f.write("=" * 60 + "\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 60 + "\n\n")

        f.write("KEY METRICS\n")
        f.write("-" * 60 + "\n\n")

        f.write(f"1. Total Revenue:           ${total_revenue:,.2f}\n")
        f.write(f"2. Total Orders:            {total_orders:,}\n")
        f.write(f"3. Total Customers:         {total_customers:,}\n")
        f.write(f"4. Average Order Value:     ${avg_order_value:,.2f}\n")
        f.write(f"5. Best Selling Category:   {best_category[0]} (${best_category[1]:,.2f})\n")
        f.write(f"6. Most Valuable Customer:  {top_customer[0]} (${top_customer[1]:,.2f})\n\n")

        f.write("=" * 60 + "\n")
        f.write("End of Report\n")
        f.write("=" * 60 + "\n")

    print(f"✓ Summary report generated: {output_file}")


def main():
    """Main function to generate reports."""
    DB_PATH = "data/myproject.db"

    print("=" * 60)
    print("REPORT GENERATION")
    print("=" * 60 + "\n")

    # Export top products to CSV
    print("1. Exporting top products to CSV...")
    top_products = get_top_products(DB_PATH, limit=10)
    export_to_csv(
        top_products,
        "top_products.csv",
        ["Product Name", "Category", "Units Sold", "Total Revenue"]
    )

    # Generate summary report
    print("\n2. Generating summary text report...")
    generate_summary_report(DB_PATH)

    print("\n" + "=" * 60)
    print("✓ All reports generated successfully!")
    print("=" * 60)
    print("\nGenerated files:")
    print("  - top_products.csv")
    print("  - report.txt")


if __name__ == "__main__":
    main()
