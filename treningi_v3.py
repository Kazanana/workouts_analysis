import re
from datetime import datetime
import sqlite3
# separation into sigle workouts using regex was done using ChatGPT
def split_workouts(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    pattern = r'(\d{2}\.\d{2}\.\d{4} .+?)(?=(\d{2}\.\d{2}\.\d{4} )|\Z)'

    matches = re.findall(pattern, content, re.DOTALL)
    
    entries = [match[0].strip() for match in matches]
    
    return entries

def insert_WorkoutComment(date,place, dry_run = True):
    if dry_run:
        query = "INSERT INTO WorkoutComment (date, comment) VALUES (?, ?)"
        data = (date, place)
        print(f"Query: {query}\n Data: {data}")
    else:
        query = "INSERT INTO WorkoutComment (date, comment) VALUES (?, ?)"
        data = (date, place)
        cursor.execute(query, data)
        conn.commit()

def insert_training_log(exercise_name,date,reps,weight, dry_run = True):
    # reps and weight
    if dry_run:
        query = "insert into training_log (exercise_id,date,reps,metric_weight) values(?,?,?,?);"
        data = (exercise_id, date, reps, weight)
        print(f"Query: {query}\n Data: {data}")
    else:
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

exercise_dict = {"exercises": [
    {
        "name": "Chest Dip",
        "regex": r'dip:|Dip:|dipy:|Dipy:'
    },
    {
        "name": "Pull Up",
        "regex": r'Pull up:|pull up:'
    },
    {
        "name": "Handstand Pushup",
        "regex": r'(?!.*ściana)(Hs|HS) (pu|push up|Pu)'
    },
    {
        "name": "Handstand Pushup Wall",
        "regex": r'(Hs|HS) (pu|push up|Pu).*ściana'
    },
    {
        "name": "Muscle Up",
        "regex": r'Muscle up'
    },
    {
        "name": "Chin Up",
        "regex": r'Chin up'
    },
    {
        "name": "Barbell Squat",
        "regex": r'Przysiad'
    },
    {
        "name": "Neutral Chin Up",
        "regex": r'Neutral'
    },
    {
        "name": "Handstand",
        "regex": r'(?!.*:).*hs.*|(?!.*:).*HS.*|(?!.*:).*Hs.*'
    }
]}

for entry in exercise_entries:
    # need to split like that because entry is a string
    date_and_place = entry.splitlines()[0]
    exercises = entry.splitlines()[1:]

    date = date_and_place.split(' ', 1)[0]
    date = date.replace('.','-')
    date = datetime.strptime(date, "%d-%m-%Y").strftime("%Y-%m-%d")

    place = date_and_place.split(' ', 1)[1]
    print(date_and_place)
    # insert insert_WorkoutComment(data, place)
    for ex in exercises:
        matches_ChestDip = re.findall(r'dip:|Dip:|dipy:|Dipy:', ex)
        matches_PullUp = re.findall(r'Pull up:|pull up:', ex)
        matches_HS_PU = re.findall(r'(?!.*ściana)(Hs|HS) (pu|push up|Pu)', ex)
        matches_HS_PU_Wall = re.findall(r'(Hs|HS) (pu|push up|Pu).*ściana', ex)
        matches_MuscleUp = re.findall(r'Muscle up', ex)
        matches_ChinUp = re.findall(r'Chin up', ex)
        matches_BarbellSquat = re.findall(r'Przysiad', ex)
        matches_NeutralChinUp = re.findall(r'Neutral', ex)
        matches_HS = re.findall(r'(?!.*:).*hs.*|(?!.*:).*HS.*|(?!.*:).*Hs.*', ex)

        if matches_ChestDip:
            print(split_sets_into_reps(ex))
        elif matches_PullUp:
            print(split_sets_into_reps(ex))
        elif matches_HS_PU:
            print(split_sets_into_reps(ex))
        elif matches_HS_PU_Wall:
            print(split_sets_into_reps(ex))
        elif matches_MuscleUp:
            print(split_sets_into_reps(ex))
        elif matches_ChinUp:
            print(split_sets_into_reps(ex))
        elif matches_BarbellSquat:
            print(split_sets_into_reps(ex))
        elif matches_NeutralChinUp:
            print(split_sets_into_reps(ex))
        elif matches_HS:
            print("HANDSTAND PRACTICE")
        else:
            continue

    print("-----------------------------------------------")
# insert_WorkoutComment(date, place)
# print(f"PLACE: {date_and_place}\n ENTRIES: {exercises}")

    
# conn.close()