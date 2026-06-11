import sqlite3
import pandas as pd

conn = sqlite3.connect("sales.db")

query = """
SELECT
    customer_id,
    ROUND(SUM(sales), 2) AS total_revenue,
    ROUND(SUM(cost), 2) AS total_cost,
    ROUND(SUM(sales) - SUM(cost), 2) AS contribution_margin
FROM sales_orders
GROUP BY customer_id
ORDER BY total_revenue DESC; 
"""

df = pd.read_sql(query, conn)

print("\nTOP 20 CUSTOMERS BY REVENUE\n")
print(df.head(20))

conn.close()