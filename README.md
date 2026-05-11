# Retail Analytics Warehouse

## Overview

Retail Analytics Warehouse is an end-to-end analytics engineering portfolio project built using Python, DuckDB, SQL, and Streamlit.

The project demonstrates how raw retail transaction data can be transformed into a structured warehouse architecture using staging tables, star schema modeling, analytics marts, and dashboard visualisation.

The pipeline includes:

- raw data ingestion
- ELT-style warehouse transformations
- star schema implementation
- fact and dimension modeling
- analytics marts
- data quality testing
- logging
- interactive dashboard analytics

---

## Project Goals

This project was built to learn and demonstrate:

- Data warehouse architecture
- ETL / ELT workflows
- SQL transformation pipelines
- Star schema modeling
- Fact and dimension table design
- Analytics engineering concepts
- Dashboard development
- Data quality validation
- Production-style project structure

---

## Architecture

```text
                +------------------+
                |   Raw CSV Data   |
                +------------------+
                          |
                          v
                +------------------+
                |   Python Loader  |
                |    load.py       |
                +------------------+
                          |
                          v
                +------------------+
                |    raw_sales     |
                +------------------+
                          |
                          v
                +------------------+
                |    stg_sales     |
                +------------------+
                          |
          +---------------+---------------+
          |               |               |
          v               v               v
+----------------+ +----------------+ +----------------+
| dim_customer   | | dim_product    | | dim_country    |
+----------------+ +----------------+ +----------------+
                          |
                          v
                +------------------+
                |    fact_sales    |
                +------------------+
                          |
                          v
                +------------------+
                | Analytics Marts  |
                +------------------+
                          |
                          v
                +------------------+
                | Streamlit App    |
                +------------------+
```

---

## Dashboard Preview

The Streamlit dashboard provides interactive analytics powered by the warehouse star schema.

### Dashboard Overview

Shows:
- KPI cards
- monthly revenue trends
- customer metrics
- product performance

![Dashboard Overview](docs/screenshots/image.png)

---

### Filter Panel

Users can dynamically filter:
- date range
- country
- products

This simulates a lightweight BI-style analytics experience.

![Filters](docs/screenshots/Filter.png)

---

### Top Customers

Displays the highest revenue-generating customers with:
- total revenue
- total orders
- quantity purchased

![Top Customers](docs/screenshots/top_customer.png)

---

### Top Products

Displays the highest-performing products by revenue.

![Top Products](docs/screenshots/top_product.png)

---

### Product Revenue Distribution

Additional product-level analytics visualisation.

![Product Revenue Distribution](docs/screenshots/top_product2.png)

---

### Transaction Details

Detailed transaction-level analytics table powered by the fact table.

![Transaction Details](docs/screenshots/Transaction_detail.png)

---

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Data pipeline |
| Pandas | Data loading |
| DuckDB | Analytical database |
| SQL | Data transformation |
| Streamlit | Dashboard |
| Logging | Pipeline monitoring |
| Git/GitHub | Version control |

---

## Project Structure

```text
retail-analytics-warehouse/
│
├── app/
│   └── dashboard.py
│
├── data/
│   └── raw/
│
├── database/
│   └── retail_warehouse.duckdb
│
├── docs/
│   ├── architecture.md
│   ├── learning_notes.md
│   └── screenshots/
│
├── sql/
│   └── 01_check_tables.sql
│
├── src/
│   ├── load.py
│   ├── logger.py
│   └── transform.py
│
├── testing/
│   ├── test_data_quality.py
│   └── test_db.py
│
├── .gitignore
├── main.py
├── README.md
└── requirements.txt
```

---

## Data Warehouse Layers

### Raw Layer

Stores the original source data with minimal modification.

### Staging Layer

The staging layer:
- standardises column names
- handles missing values
- converts data types
- calculates revenue metrics

### Dimension Tables

Dimension tables provide descriptive business context:

- `dim_customer`
- `dim_product`
- `dim_country`
- `dim_date`

### Fact Table

The `fact_sales` table stores measurable business events including:
- quantity sold
- revenue
- pricing metrics

### Analytics Marts

Business-ready analytics tables for reporting and dashboards.

---

## Current Features

- Load raw retail CSV data
- Build warehouse tables using DuckDB
- Create star schema
- Generate analytics marts
- Interactive Streamlit dashboard
- KPI visualisation
- Data quality validation
- Logging system
- SQL-based transformations

---

## Current KPIs

The dashboard currently displays:

- Total revenue
- Total orders
- Unique customers
- Units sold
- Average order value
- Monthly revenue trends
- Product performance
- Country-level revenue
- Top customers

---

## Example SQL Transformation

```sql
CREATE OR REPLACE TABLE mart_monthly_sales AS

SELECT
    d.month_start AS sales_month,
    SUM(f.revenue) AS total_revenue,
    SUM(f.quantity) AS total_quantity,
    COUNT(DISTINCT f.invoice_no) AS total_orders,
    COUNT(DISTINCT f.customer_key) AS unique_customers

FROM fact_sales f

LEFT JOIN dim_date d
    ON f.date_key = d.date_key

GROUP BY 1
ORDER BY 1;
```

---

## Data Quality Tests

The project includes automated validation checks for:

- required table existence
- negative quantities
- negative prices
- null revenue values
- fact table row consistency
- missing dimension keys

---

## Logging

The pipeline uses Python logging to provide:
- execution tracking
- debugging visibility
- operational monitoring

Example:

```text
2026-05-11 12:09:09 | INFO | Analytics tables created successfully.
```

---

## How To Run

### 1. Create environment

```bash
conda create -n retail_warehouse python=3.11 -y
conda activate retail_warehouse
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run warehouse pipeline

```bash
python main.py
```

### 4. Run dashboard

```bash
streamlit run app/dashboard.py
```

---

## Problems Solved During Development

### Date parsing issue

The raw dataset used:

```text
MM/DD/YYYY HH:MM
```

This required using DuckDB `STRPTIME()` before converting to DATE.

### Missing customer IDs

Customer IDs contained null values and numeric types, requiring explicit casting before null replacement.

### Column naming mismatches

The source dataset used inconsistent column names such as:
- `InvoiceNo`
- `UnitPrice`

These were standardised during the staging process.

### Dependency ordering

Analytics marts depended on the `fact_sales` table, requiring proper transformation sequencing.

---

## Future Improvements

Planned upgrades:

- dbt integration
- Docker support
- CI/CD pipeline
- Snowflake migration
- Advanced dashboard styling
- Customer segmentation
- Sales forecasting
- Incremental loading
- Data lineage tracking
- Automated scheduling
- Advanced warehouse testing

---

## Learning Outcomes

This project helped develop practical understanding of:

- ETL / ELT workflows
- Data warehouse architecture
- Star schema modeling
- SQL transformations
- Analytics engineering
- Data quality testing
- Logging systems
- Dashboard development
- Real-world debugging
- Project structuring

---

## Author

Nguyen Ha Duong  
Master of Data Science — Swinburne University of Technology