"""
Data Analysis Script
This script performs 5 analytical queries on the e-commerce database.

Queries 1-2: SQL only
Queries 3-5: Both SQL and Python versions to demonstrate different approaches
"""

import sqlite3


# ============================================
# QUERY 1: Basic SELECT with WHERE (SQL only)
# ============================================

def query1_customers_by_city(db_path, city):
    """Find all customers from a specific city.

    Business question: Which customers are in Boston for local marketing?

    Args:
        db_path (str): Path to the database
        city (str): City name to filter by

    Returns:
        list: List of customer records from the specified city
    """
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        results = cursor.execute(
            "SELECT * FROM customers WHERE city = ?",
            (city,)
        ).fetchall()
    return results


# ============================================
# QUERY 2: JOIN tables (SQL only)
# ============================================

def query2_revenue_by_category(db_path):
    """Calculate total revenue by product category.

    Business question: Which product categories generate the most revenue?

    Returns:
        list: List of tuples (category, total_revenue) sorted by revenue descending
    """
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        results = cursor.execute('''
            SELECT
                p.category,
                SUM(o.quantity * p.price) AS total_revenue
            FROM orders o
            JOIN products p ON o.product_id = p.product_id
            GROUP BY p.category
            ORDER BY total_revenue DESC
        ''').fetchall()
    return results


# ============================================
# QUERY 3: Top customers by spending
# (Both SQL and Python versions)
# ============================================

def query3_top_customers_sql(db_path, limit=5):
    """Find top N customers by total spending - SQL VERSION.

    Business question: Who are our most valuable customers?

    Args:
        db_path (str): Path to the database
        limit (int): Number of top customers to return

    Returns:
        list: List of tuples (customer_id, name, total_spent)
    """
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        results = cursor.execute('''
            SELECT
                c.customer_id,
                c.name,
                SUM(o.quantity * p.price) AS total_spent
            FROM customers c
            JOIN orders o ON c.customer_id = o.customer_id
            JOIN products p ON o.product_id = p.product_id
            GROUP BY c.customer_id, c.name
            ORDER BY total_spent DESC
            LIMIT ?
        ''', (limit,)).fetchall()
    return results


def query3_top_customers_python(db_path, limit=5):
    """Find top N customers by total spending - PYTHON VERSION.

    Uses simple SQL to get data, then processes in Python using:
    - Dictionaries to group by customer
    - Loops to calculate totals
    - sorted() function to order results

    Args:
        db_path (str): Path to the database
        limit (int): Number of top customers to return

    Returns:
        list: List of tuples (customer_id, name, total_spent)
    """
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        # Get raw data with JOIN (no GROUP BY or aggregations)
        raw_data = cursor.execute('''
            SELECT
                c.customer_id,
                c.name,
                o.quantity,
                p.price
            FROM customers c
            JOIN orders o ON c.customer_id = o.customer_id
            JOIN products p ON o.product_id = p.product_id
        ''').fetchall()

    # Process in Python
    customer_spending = {}  # Dictionary to track spending per customer

    # Loop through data and calculate totals
    for customer_id, name, quantity, price in raw_data:
        order_value = quantity * price

        if customer_id not in customer_spending:
            customer_spending[customer_id] = {
                'name': name,
                'total_spent': 0
            }

        customer_spending[customer_id]['total_spent'] += order_value

    # Convert dictionary to list of tuples
    results = [
        (customer_id, data['name'], data['total_spent'])
        for customer_id, data in customer_spending.items()
    ]

    # Sort by total_spent descending and limit results
    results = sorted(results, key=lambda x: x[2], reverse=True)[:limit]

    return results


# ============================================
# QUERY 4: Monthly sales trend
# (Both SQL and Python versions)
# ============================================

def query4_monthly_sales_sql(db_path):
    """Calculate monthly sales trend - SQL VERSION.

    Business question: How are our sales trending over time?

    Returns:
        list: List of tuples (year_month, total_revenue, order_count)
    """
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        results = cursor.execute('''
            SELECT
                strftime('%Y-%m', o.order_date) AS year_month,
                SUM(o.quantity * p.price) AS total_revenue,
                COUNT(o.order_id) AS order_count
            FROM orders o
            JOIN products p ON o.product_id = p.product_id
            GROUP BY year_month
            ORDER BY year_month
        ''').fetchall()
    return results


def query4_monthly_sales_python(db_path):
    """Calculate monthly sales trend - PYTHON VERSION.

    Uses simple SQL to get data, then processes in Python using:
    - String slicing to extract year-month
    - Dictionary to group by month
    - Loops to calculate totals
    - sorted() to order chronologically

    Returns:
        list: List of tuples (year_month, total_revenue, order_count)
    """
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        # Get raw data with JOIN (no GROUP BY)
        raw_data = cursor.execute('''
            SELECT
                o.order_date,
                o.quantity,
                p.price
            FROM orders o
            JOIN products p ON o.product_id = p.product_id
        ''').fetchall()

    # Process in Python
    monthly_sales = {}  # Dictionary to track sales per month

    # Loop through data
    for order_date, quantity, price in raw_data:
        # Extract year-month from date string (format: YYYY-MM-DD)
        year_month = order_date[:7]  # Gets 'YYYY-MM'
        order_value = quantity * price

        if year_month not in monthly_sales:
            monthly_sales[year_month] = {
                'total_revenue': 0,
                'order_count': 0
            }

        monthly_sales[year_month]['total_revenue'] += order_value
        monthly_sales[year_month]['order_count'] += 1

    # Convert to list of tuples
    results = [
        (month, data['total_revenue'], data['order_count'])
        for month, data in monthly_sales.items()
    ]

    # Sort chronologically
    results = sorted(results, key=lambda x: x[0])

    return results


# ============================================
# QUERY 5: Customer purchase frequency analysis
# (Both SQL and Python versions)
# ============================================

def query5_customer_engagement_sql(db_path, limit=10):
    """Analyze customer purchase frequency and average order size - SQL VERSION.

    Business question: Which customers are most engaged (frequent buyers with high order values)?

    This helps identify:
    - Repeat customers vs one-time buyers
    - Customers who buy frequently but in small quantities vs bulk buyers
    - Best targets for loyalty programs

    Args:
        db_path (str): Path to the database
        limit (int): Number of top customers to return

    Returns:
        list: List of tuples (customer_name, city, order_count, total_items, avg_items_per_order, total_spent)
    """
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        results = cursor.execute('''
            SELECT
                c.name,
                c.city,
                COUNT(DISTINCT o.order_id) AS order_count,
                SUM(o.quantity) AS total_items,
                ROUND(CAST(SUM(o.quantity) AS FLOAT) / COUNT(DISTINCT o.order_id), 2) AS avg_items_per_order,
                SUM(o.quantity * p.price) AS total_spent
            FROM customers c
            JOIN orders o ON c.customer_id = o.customer_id
            JOIN products p ON o.product_id = p.product_id
            GROUP BY c.customer_id, c.name, c.city
            ORDER BY order_count DESC, total_spent DESC
            LIMIT ?
        ''', (limit,)).fetchall()
    return results


def query5_customer_engagement_python(db_path, limit=10):
    """Analyze customer purchase frequency and average order size - PYTHON VERSION.

    Uses simple SQL to get data, then processes in Python using:
    - Dictionary to group by customer
    - Set to track unique orders per customer
    - Loops to calculate totals and averages
    - sorted() with multiple sort keys

    Args:
        db_path (str): Path to the database
        limit (int): Number of top customers to return

    Returns:
        list: List of tuples (customer_name, city, order_count, total_items, avg_items_per_order, total_spent)
    """
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        # Get raw data with JOIN
        raw_data = cursor.execute('''
            SELECT
                c.customer_id,
                c.name,
                c.city,
                o.order_id,
                o.quantity,
                p.price
            FROM customers c
            JOIN orders o ON c.customer_id = o.customer_id
            JOIN products p ON o.product_id = p.product_id
        ''').fetchall()

    # Process in Python
    customer_stats = {}  # Dictionary to track stats per customer

    # Loop through data and calculate metrics
    for customer_id, name, city, order_id, quantity, price in raw_data:
        if customer_id not in customer_stats:
            customer_stats[customer_id] = {
                'name': name,
                'city': city,
                'orders': set(),  # Use set to track unique order IDs
                'total_items': 0,
                'total_spent': 0
            }

        # Track unique orders
        customer_stats[customer_id]['orders'].add(order_id)
        customer_stats[customer_id]['total_items'] += quantity
        customer_stats[customer_id]['total_spent'] += quantity * price

    # Convert to list of tuples with calculated averages
    results = []
    for customer_id, data in customer_stats.items():
        order_count = len(data['orders'])
        total_items = data['total_items']
        avg_items_per_order = round(total_items / order_count, 2) if order_count > 0 else 0
        total_spent = data['total_spent']

        results.append((
            data['name'],
            data['city'],
            order_count,
            total_items,
            avg_items_per_order,
            total_spent
        ))

    # Sort by order_count (descending), then by total_spent (descending)
    results = sorted(results, key=lambda x: (x[2], x[5]), reverse=True)[:limit]

    return results


# ============================================
# MAIN FUNCTION
# ============================================

def main():
    """Main function to run all queries and display results."""
    DB_PATH = "data/myproject.db"

    print("=" * 80)
    print("E-COMMERCE DATA ANALYSIS")
    print("=" * 80)

    # Query 1: Customers by city
    print("\n1. CUSTOMERS IN BOSTON (Basic SELECT with WHERE)")
    print("-" * 80)
    results = query1_customers_by_city(DB_PATH, "Boston")
    print(f"Found {len(results)} customers in Boston:")
    for row in results[:5]:  # Show first 5
        print(f"  ID: {row[0]}, Name: {row[1]}, Email: {row[2]}")
    if len(results) > 5:
        print(f"  ... and {len(results) - 5} more")

    # Query 2: Revenue by category
    print("\n2. REVENUE BY PRODUCT CATEGORY (JOIN)")
    print("-" * 80)
    results = query2_revenue_by_category(DB_PATH)
    print(f"{'Category':<20} {'Total Revenue':>15}")
    print("-" * 40)
    for category, revenue in results:
        print(f"{category:<20} ${revenue:>14,.2f}")

    # Query 3: Top customers (both versions)
    print("\n3. TOP 5 CUSTOMERS BY SPENDING (GROUP BY - SQL & Python)")
    print("-" * 80)

    print("\nSQL VERSION:")
    sql_results = query3_top_customers_sql(DB_PATH, 5)
    print(f"{'ID':<5} {'Name':<20} {'Total Spent':>15}")
    print("-" * 45)
    for customer_id, name, total_spent in sql_results:
        print(f"{customer_id:<5} {name:<20} ${total_spent:>14,.2f}")

    print("\nPYTHON VERSION:")
    python_results = query3_top_customers_python(DB_PATH, 5)
    print(f"{'ID':<5} {'Name':<20} {'Total Spent':>15}")
    print("-" * 45)
    for customer_id, name, total_spent in python_results:
        print(f"{customer_id:<5} {name:<20} ${total_spent:>14,.2f}")

    # Query 4: Monthly sales trend (both versions)
    print("\n4. MONTHLY SALES TREND (Date Functions & GROUP BY - SQL & Python)")
    print("-" * 80)

    print("\nSQL VERSION (First 6 months):")
    sql_results = query4_monthly_sales_sql(DB_PATH)
    print(f"{'Month':<10} {'Revenue':>15} {'Orders':>10}")
    print("-" * 40)
    for month, revenue, count in sql_results[:6]:
        print(f"{month:<10} ${revenue:>14,.2f} {count:>10}")

    print("\nPYTHON VERSION (First 6 months):")
    python_results = query4_monthly_sales_python(DB_PATH)
    print(f"{'Month':<10} {'Revenue':>15} {'Orders':>10}")
    print("-" * 40)
    for month, revenue, count in python_results[:6]:
        print(f"{month:<10} ${revenue:>14,.2f} {count:>10}")

    # Query 5: Customer engagement analysis (both versions)
    print("\n5. CUSTOMER PURCHASE FREQUENCY ANALYSIS (Custom Analysis - SQL & Python)")
    print("-" * 80)
    print("Business question: Which customers are most engaged (repeat buyers)?")

    print("\nSQL VERSION:")
    sql_results = query5_customer_engagement_sql(DB_PATH, 10)
    print(f"{'Customer':<20} {'City':<15} {'Orders':>8} {'Items':>8} {'Avg/Order':>10} {'Total Spent':>12}")
    print("-" * 85)
    for name, city, orders, items, avg_items, spent in sql_results:
        print(f"{name:<20} {city:<15} {orders:>8} {items:>8} {avg_items:>10.2f} ${spent:>11,.2f}")

    print("\nPYTHON VERSION:")
    python_results = query5_customer_engagement_python(DB_PATH, 10)
    print(f"{'Customer':<20} {'City':<15} {'Orders':>8} {'Items':>8} {'Avg/Order':>10} {'Total Spent':>12}")
    print("-" * 85)
    for name, city, orders, items, avg_items, spent in python_results:
        print(f"{name:<20} {city:<15} {orders:>8} {items:>8} {avg_items:>10.2f} ${spent:>11,.2f}")

    print("\n" + "=" * 80)
    print("✓ Analysis complete!")
    print("=" * 80)


if __name__ == "__main__":
    main()
