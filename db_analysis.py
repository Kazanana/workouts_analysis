import sqlite3

# Specify your database file
db_path = "FitNotes_Backup_2024_11_30_20_44_12.fitnotes"
date_to_find = "2024-11-18"

# Connect to the database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Get all table names
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = [row[0] for row in cursor.fetchall()]

# Find tables with a 'date' column and query for rows with the specified date
for table in tables:
    cursor.execute(f"PRAGMA table_info({table});")
    columns = cursor.fetchall()
    date_columns = [col[1] for col in columns if col[2].lower() == "date" or col[1].lower() == 'date']
    
    if date_columns:
        print(f"Table '{table}' has date columns: {date_columns}")
        for col in date_columns:
            query = f"SELECT * FROM {table} WHERE {col} = ?;"
            cursor.execute(query, (date_to_find,))
            rows = cursor.fetchall()
            if rows:
                print(f"Rows from {table} with {col} = {date_to_find}:")
                for row in rows:
                    print(row)
            else:
                print(f"No rows found in {table} with {col} = {date_to_find}.")

# Close the connection
conn.close()
