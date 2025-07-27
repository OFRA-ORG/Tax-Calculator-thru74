import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('tmd_nm-26-#-ext-#.dumpdb')  # Replace 'your_database.db' with your database file
cursor = conn.cursor()

tables = ["base", "baseline", "reform"]

# 1. Get column names
for table in tables:
    cursor.execute(f"PRAGMA table_info({table})")
    column_info = cursor.fetchall()
    column_names = [info[1] for info in column_info]  # Extracting the column names from the result
    print(f"Column Names for {table}:", column_names)

    cursor.execute(f"SELECT * FROM {table} LIMIT 10")
    records = cursor.fetchall()
    print("\nFirst 10 Records:")
    for record in records:
        print(record)

# Close the connection
conn.close()