# Retail Analytics Warehouse

## Overview

Retail Analytics Warehouse is a portfolio project that demonstrates how raw retail transaction data can be transformed into analytics-ready business insights using a modern warehouse-style pipeline.

The project uses Python, DuckDB, SQL, and Streamlit to simulate a lightweight analytics engineering workflow.

---

## Project Goals

This project was built to learn and demonstrate:

- Data warehouse concepts
- ETL pipeline development
- SQL-based data transformation
- Analytics engineering workflow
- Business KPI reporting
- Dashboard development
- GitHub project structuring

---

## Architecture

```text
Raw CSV Data
    |
    v
Python ETL Pipeline
    |
    v
DuckDB Database
    |
    v
Staging Tables
    |
    v
Analytics Mart Tables
    |
    v
Streamlit Dashboard
```

---

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Data pipeline |
| Pandas | Data loading |
| DuckDB | Analytical database |
| SQL | Data transformation |
| Streamlit | Dashboard |
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
│   └── learning_notes.md
│
├── sql/
│   └── 01_check_tables.sql
│
├── src/
│   ├── load.py
│   └── transform.py
│
├── testing/
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

Stores the original retail dataset with minimal modification.

### Staging Layer

Cleans and standardises:
- column names
- data types
- null values
- calculated revenue fields

### Mart Layer

Creates business-ready analytics tables such as:
- monthly sales
- product performance
- customer metrics

---

## Features

- Load raw CSV retail data
- Store data in DuckDB
- Build staging and analytics tables
- Calculate KPIs
- Visualise metrics in Streamlit
- Query warehouse tables using SQL

---

## Current KPIs

The dashboard currently displays:

- Total revenue
- Total orders
- Unique customers
- Monthly revenue trends
- Top products by revenue

---

## Example SQL

```sql
SELECT
    DATE_TRUNC('month', invoice_date) AS sales_month,
    SUM(revenue) AS total_revenue
FROM stg_sales
GROUP BY 1
ORDER BY 1;
```

---

## How To Run

### 1. Create environment

```bash
conda create -n retail_warehouse python=3.11 -y
conda activate retail_warehouse
```

### 2. Install requirements

```bash
pip install -r requirements.txt
```

### 3. Run pipeline

```bash
python main.py
```

### 4. Start dashboard

```bash
streamlit run app/dashboard.py
```

---

## Problems Solved During Development

### Date parsing issue

The dataset used non-standard date formatting:

```text
MM/DD/YYYY HH:MM
```

This required using DuckDB `STRPTIME()` before converting to DATE.

### Missing customer IDs

Some customer IDs were null and numeric, requiring explicit casting before null replacement.

### Column naming mismatches

The raw dataset used inconsistent column names such as:
- `InvoiceNo`
- `UnitPrice`

These were standardised in the staging layer.

---

## Future Improvements

Planned upgrades:

- Star schema design
- Fact and dimension tables
- dbt integration
- Docker support
- Snowflake migration
- Data quality tests
- Automated pipeline scheduling
- Advanced Streamlit filters
- KPI forecasting
- Customer segmentation

---

## Learning Outcomes

This project helped develop practical understanding of:

- ETL workflows
- SQL transformations
- Warehouse architecture
- Data modeling
- Analytics engineering
- Dashboard development
- Real-world debugging

---

## Author

Nguyen Ha Duong  
Master of Data Science — Swinburne University of Technology
