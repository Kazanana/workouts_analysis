import sqlite3
from datetime import datetime

db_path = "FitNotes_Backup_2024_11_30_20_44_12_TEST.fitnotes"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
date = str(datetime.now().date())

query = "INSERT INTO WorkoutComment (date, comment) VALUES (?, ?)"
data = ('2022-07-06', 'dupa')

# Execute the query with the data
cursor.execute(query, data)
conn.commit()
conn.close()