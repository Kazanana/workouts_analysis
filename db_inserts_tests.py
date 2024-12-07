import sqlite3
from datetime import datetime

db_path = "FitNotes_Backup_2024_12_07_15_14_00_TEST.fitnotes"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
date = str(datetime.now().date())

def insert_training_log(exercise_name,date,reps,weight, dry_run = True):
    # reps and weight
    if dry_run:
        cursor.execute(f"select _id from exercise where name like '{exercise_name}';")
        # response from DB is list of tuples
        exercise_id = cursor.fetchall()[0][0]
        # print(type(exercise_id[0][0])) -> int
        query = "INSERT INTO training_log (exercise_id,date,reps,metric_weight) VALUES(?,?,?,?);"
        data = (exercise_id, date, reps, weight)
        print(f"Query: {query}\n Data: {data}")
    else:
        cursor.execute(f"select _id from exercise where name like '{exercise_name}';")
        exercise_id = cursor.fetchall()
        query = "INSERT INTO training_log (exercise_id,date,reps,metric_weight) VALUES(?,?,?,?);"
        data = (exercise_id, date, reps, weight)
        cursor.execute(query, data)
        conn.commit()

# Execute the query with the data
insert_training_log("Pull Up", date, 3, 0)

conn.close()