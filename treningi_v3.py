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

def insert_WorkoutComment(date,place):

    query = "INSERT INTO WorkoutComment (date, comment) VALUES (?, ?)"
    data = (date, place)
    cursor.execute(query, data)
    conn.commit()

def insert_training_log(exercise_name,date,reps,weight):
    # reps and weight
    cursor.execute(f"select _id from exercise where name like '{exercise_name}';")
    exercise_id = cursor.fetchall()
    query = "insert into training_log (exercise_id,date,reps,metric_weight) values(?,?,?,?);"
    data = (exercise_id, date, reps, weight)
    cursor.execute(query, data)
    conn.commit()

def split_sets_into_reps(ex):
    sets_list = []
    name = ex.split(":")[0].strip()
    sets = ex.split(":")[1].split(",")
    if ex.find("x") == -1:
        # no weight
        for reps in sets:
            reps = reps.strip()
            sets_list.append((name, date, reps, 0))
    else: 
        # weighted
        for set in sets:
            set = set.strip()
            weight = set.split("x")[0]
            reps = set.split("x")[1]
            sets_list.append((name, date, reps, weight))
    return sets_list

file_path = 'workouts.txt'
exercise_entries = split_workouts(file_path)

# db_path = "FitNotes_Backup_2024_11_30_20_44_12_TEST.fitnotes"
# conn = sqlite3.connect(db_path)
# cursor = conn.cursor()

for entry in exercise_entries:
    # need to split like that because entry is a string
    date_and_place = entry.splitlines()[0]
    exercises = entry.splitlines()[1:]

    date = date_and_place.split(' ', 1)[0]
    date = date.replace('.','-')
    date = datetime.strptime(date, "%d-%m-%Y").strftime("%Y-%m-%d")

    place = date_and_place.split(' ', 1)[1]
    print(date_and_place)
    for ex in exercises:
        matches_dip = re.findall(r'dip:|Dip:|dipy:|Dipy:', ex)
        matches_pullup = re.findall(r'Pull up:|pull up:', ex)
        if matches_dip:
            print(split_sets_into_reps(ex))
        elif matches_pullup:
            print(split_sets_into_reps(ex))
    print("-----------------------------------------------")
# insert_WorkoutComment(date, place)
# print(f"PLACE: {date_and_place}\n ENTRIES: {exercises}")

    
# conn.close()