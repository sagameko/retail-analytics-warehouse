SELECT
    ROW_NUMBER() OVER (ORDER BY product_code, product_name) AS product_key,
    product_code,
    product_name
FROM (
    SELECT DISTINCT
        product_code,
        product_name
    FROM {{ ref('stg_sales') }}
)