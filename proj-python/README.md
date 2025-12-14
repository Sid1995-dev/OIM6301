# Python Final Project - OIM6301

E-commerce data analysis with Python, SQLite, and API integration.

## Project Structure

```
proj-python/
├── data/
│   ├── customers.csv
│   ├── products.csv
│   ├── orders.csv
│   └── myproject.db          (generated)
├── setup_database.py         (Part 1.1)
├── analyze_data.py           (Part 1.2)
├── generate_report.py        (Part 1.3)
├── api_demo.py               (Part 2)
├── api_integration.py
├── reflection.md             (Part 3)
├── requirements.txt
└── README.md
```

## Requirements

- Python 3.7+
- No packages to install (uses standard library only)

## How to Run

```bash
cd proj-python

# 1. Setup database
python setup_database.py

# 2. Run analysis
python analyze_data.py

# 3. Generate reports
python generate_report.py

# 4. API demo
python api_demo.py

# 5. API integration
python api_integration.py
```

## What Each Script Does

**setup_database.py**
- Creates SQLite database with 3 tables (customers, products, orders)
- Imports CSV data
- Verifies import success

**analyze_data.py**
- 5 analytical queries
- Query 1-2: SQL only
- Query 3-5: Both SQL and Python versions

**generate_report.py**
- Exports `top_products.csv`
- Generates `report.txt` with summary statistics

**api_demo.py**
- Interactive country information lookup
- Uses REST Countries API (no auth required)

**api_integration.py**
- Combines database data with timezone API
- Shows customer distribution across time zones
- Demonstrates practical API integration

## Troubleshooting

**Database not found**: Run `setup_database.py` first

**API errors**: Check internet connection
