import sqlite3
import pandas as pd

conn = sqlite3.connect("sales.db")

query = """
WITH monthly_revenue AS (
    SELECT
        strftime('%Y-%m', order_date) AS month,
        SUM(sales) AS revenue
    FROM sales_orders
    GROUP BY month
)

SELECT
    month,
    ROUND(revenue,2) AS revenue,

    ROUND(
        revenue -
        LAG(revenue) OVER (
            ORDER BY month
        ),
        2
    ) AS mom_change,

    ROUND(
        (
            revenue -
            LAG(revenue) OVER (
                ORDER BY month
            )
        ) * 100.0 /
        LAG(revenue) OVER (
            ORDER BY month
        ),
        2
    ) AS mom_growth_pct

FROM monthly_revenue
ORDER BY month;
"""

df = pd.read_sql(query, conn)

print("\nMONTH-OVER-MONTH REVENUE TREND\n")
print(df)

conn.close()