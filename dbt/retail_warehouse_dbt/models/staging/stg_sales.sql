SELECT
    InvoiceNo AS invoice_no,

    CAST(
        STRPTIME(InvoiceDate, '%m/%d/%Y %H:%M')
        AS DATE
    ) AS invoice_date,

    COALESCE(
        CAST(CustomerID AS VARCHAR),
        'UNKNOWN'
    ) AS customer_id,

    Country AS country,
    StockCode AS product_code,
    Description AS product_name,

    CAST(Quantity AS INTEGER) AS quantity,
    CAST(UnitPrice AS DOUBLE) AS unit_price,

    CAST(Quantity AS INTEGER) * CAST(UnitPrice AS DOUBLE) AS revenue

FROM raw_sales

WHERE Quantity > 0
  AND UnitPrice > 0