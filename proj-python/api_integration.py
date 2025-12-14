"""
Integrates external API data with database queries.

This script fetches current time information for cities where customers are located,
which could be useful for:
- Scheduling marketing campaigns at optimal times
- Understanding customer time zones for support hours
- Analyzing geographic distribution of customer base
"""

import sqlite3
import urllib.request
import urllib.error
import json


def get_cities_from_database(db_path):
    """Get unique cities from customer database.

    Args:
        db_path (str): Path to the database

    Returns:
        list: List of tuples (city, customer_count)
    """
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        results = cursor.execute('''
            SELECT city, COUNT(*) as customer_count
            FROM customers
            GROUP BY city
            ORDER BY customer_count DESC
        ''').fetchall()
    return results


def fetch_timezone_info(city):
    """Fetch timezone and current time information for a city.

    Uses WorldTimeAPI (free, no authentication required)
    API: http://worldtimeapi.org/

    Args:
        city (str): City name

    Returns:
        dict: Timezone information or None if error
    """
    try:
        # Map city names to timezone identifiers
        city_timezone_map = {
            'Boston': 'America/New_York',
            'New York': 'America/New_York',
            'Chicago': 'America/Chicago',
            'San Francisco': 'America/Los_Angeles'
        }

        timezone = city_timezone_map.get(city)
        if not timezone:
            return None

        url = f"http://worldtimeapi.org/api/timezone/{timezone}"

        with urllib.request.urlopen(url, timeout=5) as response:
            data = json.loads(response.read().decode())

        return {
            'city': city,
            'timezone': data.get('timezone', 'N/A'),
            'datetime': data.get('datetime', 'N/A')[:19],  # Get YYYY-MM-DD HH:MM:SS
            'utc_offset': data.get('utc_offset', 'N/A'),
            'day_of_week': data.get('day_of_week', 'N/A')
        }

    except urllib.error.URLError as e:
        print(f"  API Error for {city}: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"  JSON Error for {city}: {e}")
        return None
    except Exception as e:
        print(f"  Unexpected error for {city}: {e}")
        return None


def get_customer_summary_by_city(db_path):
    """Get customer summary with revenue for each city.

    Args:
        db_path (str): Path to the database

    Returns:
        list: List of tuples (city, customer_count, total_revenue, avg_revenue_per_customer)
    """
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        results = cursor.execute('''
            SELECT
                c.city,
                COUNT(DISTINCT c.customer_id) as customer_count,
                SUM(o.quantity * p.price) as total_revenue,
                ROUND(SUM(o.quantity * p.price) / COUNT(DISTINCT c.customer_id), 2) as avg_per_customer
            FROM customers c
            JOIN orders o ON c.customer_id = o.customer_id
            JOIN products p ON o.product_id = p.product_id
            GROUP BY c.city
            ORDER BY total_revenue DESC
        ''').fetchall()
    return results


def main():
    """Main function to demonstrate API integration with database."""
    DB_PATH = "data/myproject.db"

    print("=" * 80)
    print("API INTEGRATION - CUSTOMER GEOGRAPHIC ANALYSIS")
    print("=" * 80)
    print("\nCombining customer database with WorldTimeAPI data")
    print("Use case: Optimize marketing campaign timing across different time zones\n")

    # Get customer data from database
    print("Step 1: Analyzing customer distribution by city...")
    print("-" * 80)
    city_summary = get_customer_summary_by_city(DB_PATH)

    print(f"{'City':<20} {'Customers':>10} {'Revenue':>15} {'Avg/Customer':>15}")
    print("-" * 65)
    for city, customers, revenue, avg in city_summary:
        print(f"{city:<20} {customers:>10} ${revenue:>14,.2f} ${avg:>14,.2f}")

    # Fetch timezone information for each city
    print("\n\nStep 2: Fetching current time zone information from API...")
    print("-" * 80)

    timezone_data = []
    for city, customer_count in get_cities_from_database(DB_PATH):
        print(f"Fetching timezone info for {city}...")
        tz_info = fetch_timezone_info(city)
        if tz_info:
            tz_info['customer_count'] = customer_count
            timezone_data.append(tz_info)

    # Display integrated results
    print("\n\nStep 3: Integrated Analysis - Customer Locations with Time Zones")
    print("=" * 80)

    if timezone_data:
        print(f"{'City':<20} {'Customers':>10} {'Timezone':<25} {'UTC Offset':>12}")
        print("-" * 80)
        for data in timezone_data:
            print(f"{data['city']:<20} {data['customer_count']:>10} "
                  f"{data['timezone']:<25} {data['utc_offset']:>12}")

        print("\n" + "=" * 80)
        print("BUSINESS INSIGHTS")
        print("=" * 80)

        # Find cities in each timezone
        timezones = {}
        for data in timezone_data:
            tz = data['timezone']
            if tz not in timezones:
                timezones[tz] = []
            timezones[tz].append(data['city'])

        print("\nCustomer distribution by timezone:")
        for tz, cities in timezones.items():
            print(f"  {tz}: {', '.join(cities)}")

        print("\nRecommendations:")
        print("  - Schedule email campaigns at 9 AM local time for each timezone")
        print("  - Plan customer support hours to cover all time zones")
        print("  - Consider timezone when launching time-sensitive promotions")

    print("\n" + "=" * 80)
    print("✓ API integration demonstration complete!")
    print("=" * 80)

    print("\n" + "=" * 80)
    print("TECHNICAL NOTES")
    print("=" * 80)
    print("• Combined SQL queries with external API calls")
    print("• Used WorldTimeAPI (free, no authentication)")
    print("• Demonstrates practical business use case")
    print("• Shows how to enrich database data with external sources")


if __name__ == "__main__":
    main()
