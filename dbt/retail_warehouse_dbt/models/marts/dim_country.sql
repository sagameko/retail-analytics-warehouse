SELECT
    ROW_NUMBER() OVER (ORDER BY country) AS country_key,
    country
FROM (
    SELECT DISTINCT country
    FROM {{ ref('stg_sales') }}
)