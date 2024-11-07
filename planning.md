# Main idea
I got FitNotes app that lets me export data in a csv.
Right now I need to start using the app and if there is something that I need and app doesnt offer, I will try to manipulate csv file.

# Upload my old notes to the app
In the app there's an option to restore data from backup. Backup is in sqlite3 format. In order to automatically upload my data to app I need to create a database file from my old notes.
First I need to fill in couple of workouts to see how the database with my inputs look like. Then I need to write python script that will convert my old notes into database.
## tasks
1. Get all rows from the DB that constitute one workout

## DB analysis
training_log table has all exersizes. Columns:
_id|exercise_id|date|metric_weight|reps|unit|routine_section_exercise_set_id|timer_auto_start|is_personal_record|is_personal_record_first|is_complete|is_pending_update|distance|duration_seconds

This is 3 sets of handstand pushups
11|100|2024-10-21|0|5|0|0|0|0|0|0|0|0|0
12|100|2024-10-21|0|6|0|0|0|0|0|0|0|0|0
13|100|2024-10-21|0|5|0|0|0|0|0|0|0|0|0

sqlite> select * from WorkoutComment;
_id|date|comment
1|2024-10-25|Kangur - Two failed 50kg pull ups
2|2024-10-26|Hoża z randomami
3|2024-10-27|Drążki
4|2024-10-23|Murall
5|2024-10-22|Hoża ze znajomymi
6|2024-10-21|Kangur

List of tables to make entries:
- WorkoutComment,
- exercise,
- training_log,
- Category,
I think that after exporting existing app state there will only be a need to update training_log and WorkoutComment

Inserting 69 reps of excercise of id 100 on a given data
``` sql
insert into training_log (exercise_id,date,reps,metric_weight)
values(100,'2024-11-01',69,0);
```
map a exercise id from another table using name
```sql
select _id from exercise
where name like 'Handstand Pushups'
```
combine
```sql
insert into training_log (exercise_id,date,reps,metric_weight)
values((select _id from exercise
where name like 'Handstand Pushups'),
'2024-11-02',69,0);
```
Do this query for each excercise
## old file transformation
Need to decide what I want to choose to read
- pull ups
- pull ups + weight
- neutral
- muscle up
- handstand pushups
- handstand pushups wall
- handstand
- chin up
- dips + weight
- przysiad
