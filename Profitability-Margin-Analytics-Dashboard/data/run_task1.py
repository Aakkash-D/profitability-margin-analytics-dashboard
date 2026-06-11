import sqlite3

# Connect to database
conn = sqlite3.connect("sales.db")

# Read SQL file
with open("task1_queries.sql", "r", encoding="utf-8") as file:
    sql_script = file.read()

# Execute all queries
conn.executescript(sql_script)

print("✅ All SQL queries executed successfully!")

conn.close()