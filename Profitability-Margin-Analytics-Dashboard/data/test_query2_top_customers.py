import sqlite3
import pandas as pd

conn = sqlite3.connect("sales.db")

query = """
WITH customer_region_revenue AS (
    SELECT
        region,
        customer_id,
        SUM(sales) AS revenue
    FROM sales_orders
    GROUP BY region, customer_id
),

ranked_customers AS (
    SELECT
        region,
        customer_id,
        revenue,
        ROW_NUMBER() OVER (
            PARTITION BY region
            ORDER BY revenue DESC
        ) AS revenue_rank
    FROM customer_region_revenue
)

SELECT
    region,
    customer_id,
    ROUND(revenue,2) AS revenue,
    revenue_rank
FROM ranked_customers
WHERE revenue_rank <= 3
ORDER BY region, revenue_rank;
"""

df = pd.read_sql(query, conn)

print("\nTOP 3 CUSTOMERS BY REGION\n")
print(df)

conn.close()