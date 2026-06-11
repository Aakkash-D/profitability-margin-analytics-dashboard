import pandas as pd
import sqlite3

sales = pd.read_csv("sales_data.csv")

conn = sqlite3.connect("sales.db")

sales.to_sql(
    "sales_orders",
    conn,
    if_exists="replace",
    index=False
)

print("Database created successfully!")
print("Rows:", len(sales))

conn.close()