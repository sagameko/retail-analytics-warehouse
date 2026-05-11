SELECT
    s.invoice_no,
    d.date_key,
    c.customer_key,
    p.product_key,
    co.country_key,
    s.quantity,
    s.unit_price,
    s.revenue
FROM {{ ref('stg_sales') }} s
LEFT JOIN {{ ref('dim_date') }} d
    ON s.invoice_date = d.full_date
LEFT JOIN {{ ref('dim_customer') }} c
    ON s.customer_id = c.customer_id
LEFT JOIN {{ ref('dim_product') }} p
    ON s.product_code = p.product_code
   AND s.product_name = p.product_name
LEFT JOIN {{ ref('dim_country') }} co
    ON s.country = co.country