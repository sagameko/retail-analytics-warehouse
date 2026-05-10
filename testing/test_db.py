import duckdb

conn = duckdb.connect("database/retail_warehouse.duckdb")

tables = conn.execute("SHOW TABLES").fetchall()

print(tables)

conn.close()