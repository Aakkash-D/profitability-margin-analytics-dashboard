import sqlite3
import pandas as pd

conn = sqlite3.connect("sales.db")

query1 = """
WITH customer_revenue AS (
    SELECT
        customer_id,
        SUM(sales) AS revenue
    FROM sales_orders
    GROUP BY customer_id
)
SELECT
    ROUND(SUM(revenue),2) AS customer_total_revenue
FROM customer_revenue;
"""

query2 = """
SELECT
    ROUND(SUM(sales),2) AS overall_revenue
FROM sales_orders;
"""

customer_total = pd.read_sql(query1, conn)
overall_total = pd.read_sql(query2, conn)

print("\nCUSTOMER TOTAL REVENUE")
print(customer_total)

print("\nOVERALL REVENUE")
print(overall_total)

conn.close()