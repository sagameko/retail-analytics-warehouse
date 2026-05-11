# Learning Notes

## What I built

This project loads raw retail sales data into DuckDB, transforms it into cleaned staging tables, creates analytics marts, and displays insights in a Streamlit dashboard.

## Concepts learned

## Raw layer

The raw layer stores the original data as close as possible to the source.

## Staging layer

The staging layer standardises column names, fixes data types, handles missing values, and prepares the data for analysis.

## Mart layer

The mart layer contains business-ready tables for reporting and dashboards.

## Problems solved

## Date parsing

The raw date format was MM/DD/YYYY HH:MM, so I used `STRPTIME` before casting it to a date.

## Missing customer IDs

Customer IDs had missing values and numeric type, so I converted them to text before replacing nulls with `UNKNOWN`.

## Column naming mismatch

The raw dataset used names like `InvoiceNo` and `UnitPrice`, so the transformation code mapped them into clean names like `invoice_no` and `unit_price`.