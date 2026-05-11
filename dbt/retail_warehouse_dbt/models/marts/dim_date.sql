SELECT
    ROW_NUMBER() OVER (ORDER BY invoice_date) AS date_key,
    invoice_date AS full_date,
    EXTRACT(year FROM invoice_date) AS year,
    EXTRACT(month FROM invoice_date) AS month,
    EXTRACT(day FROM invoice_date) AS day,
    DATE_TRUNC('month', invoice_date) AS month_start
FROM (
    SELECT DISTINCT invoice_date
    FROM {{ ref('stg_sales') }}
)