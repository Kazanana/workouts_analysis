import re
from datetime import datetime
import sqlite3
# separation into sigle workouts using regex was done using ChatGPT
def split_workouts(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    
    # Regular expression to match dd.mm.yyyy format
    # This pattern matches a line with the date and place (dd.mm.yyyy place),
    # followed by one or more lines of exercises.
    pattern = r'(\d{2}\.\d{2}\.\d{4} .+?)(?=(\d{2}\.\d{2}\.\d{4} )|\Z)'
    
    # Find all matches in the file content
    matches = re.findall(pattern, content, re.DOTALL)
    
    # Extract only the full entry from each match
    entries = [match[0].strip() for match in matches]
    
    return entries

file_path = 'workouts.txt'
exercise_entries = split_workouts(file_path)

db_path = "FitNotes_Backup_2024_11_30_20_44_12_TEST.fitnotes"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

for entry in exercise_entries:
    # need to split like that because entry is a string
    date_and_place = entry.splitlines()[0]
    exercises = entry.splitlines()[1:]

    date = date_and_place.split(' ', 1)[0]
    place = date_and_place.split(' ', 1)[1]
    
    date = date.replace('.','-')
    date = datetime.strptime(date, "%d-%m-%Y").strftime("%Y-%m-%d")
    # # inserting workout comment
    # query = "INSERT INTO WorkoutComment (date, comment) VALUES (?, ?)"
    # data = (date, place)

    # cursor.execute(query, data)
    # conn.commit()
    # # print(f"PLACE: {date_and_place}\n ENTRIES: {exercises}")
    
conn.close()