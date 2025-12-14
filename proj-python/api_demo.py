"""
API Demonstration
Simple script to demonstrate API calling ability using the REST Countries API.

This script:
- Makes an interactive API call based on user input
- Parses JSON responses
- Displays results in a readable format
- Includes error handling for network and parsing errors
"""

import urllib.request
import urllib.error
import json


def fetch_country_data(country_name):
    """Fetch country information from REST Countries API.

    API: https://restcountries.com/v3.1/name/{country_name}

    Args:
        country_name (str): Name of the country to search for

    Returns:
        dict: Parsed country data, or None if error occurs
    """
    try:
        # Construct API URL
        url = f"https://restcountries.com/v3.1/name/{country_name}?fullText=true"

        print(f"\nFetching data from: {url}")

        # Make API call
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode())

        # The API returns a list of countries (in case of multiple matches)
        # We'll return the first match
        if data and len(data) > 0:
            return data[0]
        else:
            return None

    except urllib.error.HTTPError as e:
        if e.code == 404:
            print(f"Error: Country '{country_name}' not found.")
        else:
            print(f"HTTP Error: {e.code} - {e.reason}")
        return None

    except urllib.error.URLError as e:
        print(f"Network Error: {e.reason}")
        return None

    except json.JSONDecodeError as e:
        print(f"JSON parsing error: {e}")
        return None

    except Exception as e:
        print(f"Unexpected error: {e}")
        return None


def display_country_info(country_data):
    """Display country information in a readable format.

    Args:
        country_data (dict): Country data from the API
    """
    if not country_data:
        print("No data to display.")
        return

    print("\n" + "=" * 60)
    print("COUNTRY INFORMATION")
    print("=" * 60)

    # Official name
    official_name = country_data.get('name', {}).get('official', 'N/A')
    common_name = country_data.get('name', {}).get('common', 'N/A')
    print(f"\nOfficial Name:    {official_name}")
    print(f"Common Name:      {common_name}")

    # Capital
    capital = country_data.get('capital', ['N/A'])
    if isinstance(capital, list) and len(capital) > 0:
        print(f"Capital:          {capital[0]}")
    else:
        print(f"Capital:          N/A")

    # Region and subregion
    region = country_data.get('region', 'N/A')
    subregion = country_data.get('subregion', 'N/A')
    print(f"Region:           {region}")
    print(f"Subregion:        {subregion}")

    # Population
    population = country_data.get('population', 0)
    print(f"Population:       {population:,}")

    # Area
    area = country_data.get('area', 0)
    print(f"Area:             {area:,} km²")

    # Languages
    languages = country_data.get('languages', {})
    if languages:
        lang_list = ', '.join(languages.values())
        print(f"Languages:        {lang_list}")
    else:
        print(f"Languages:        N/A")

    # Currencies
    currencies = country_data.get('currencies', {})
    if currencies:
        currency_list = []
        for code, details in currencies.items():
            name = details.get('name', code)
            symbol = details.get('symbol', '')
            currency_list.append(f"{name} ({symbol})" if symbol else name)
        print(f"Currencies:       {', '.join(currency_list)}")
    else:
        print(f"Currencies:       N/A")

    # Timezones
    timezones = country_data.get('timezones', [])
    if timezones:
        print(f"Timezones:        {', '.join(timezones)}")

    # Flag emoji
    flag = country_data.get('flag', '')
    if flag:
        print(f"\nFlag:             {flag}")

    print("\n" + "=" * 60)


def main():
    """Main function to demonstrate API calls."""
    print("=" * 60)
    print("REST COUNTRIES API DEMO")
    print("=" * 60)
    print("\nThis demo uses the REST Countries API to fetch country information.")
    print("API: https://restcountries.com/")

    # Ask user for input
    country_name = input("Enter a country name (e.g., Japan, Brazil, Germany): ").strip()

    if not country_name:
        print("Error: Country name cannot be empty.")
        return

    # Fetch data from API
    print("\nFetching country data...")
    country_data = fetch_country_data(country_name)

    # Display results
    if country_data:
        display_country_info(country_data)
        print("\n✓ API demonstration complete!")
    else:
        print("\n✗ Failed to fetch country data. Please try again.")


if __name__ == "__main__":
    main()
