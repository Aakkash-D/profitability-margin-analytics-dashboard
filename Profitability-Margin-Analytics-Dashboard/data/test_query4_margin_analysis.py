import sqlite3
import pandas as pd

conn = sqlite3.connect("sales.db")

query = """
WITH customer_margin AS (
    SELECT
        customer_id,
        SUM(sales) AS revenue,
        SUM(cost) AS cost,
        SUM(sales) - SUM(cost) AS margin
    FROM sales_orders
    GROUP BY customer_id
),

lowest_margin_customers AS (
    SELECT *
    FROM customer_margin
    ORDER BY margin ASC
    LIMIT 10
)

SELECT
    l.customer_id,
    ROUND(l.margin,2) AS customer_margin,
    s.product,
    ROUND(
        SUM(s.sales - s.cost),
        2
    ) AS product_margin
FROM lowest_margin_customers l
JOIN sales_orders s
    ON l.customer_id = s.customer_id
GROUP BY
    l.customer_id,
    s.product
ORDER BY
    l.margin,
    product_margin;
"""

df = pd.read_sql(query, conn)

print("\nLOWEST MARGIN CUSTOMERS & LOSS DRIVERS\n")
print(df)

conn.close()