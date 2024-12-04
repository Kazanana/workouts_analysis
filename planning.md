# Main idea
I got FitNotes app that lets me export data in a csv.
Right now I need to start using the app and if there is something that I need and app doesnt offer, I will try to manipulate csv file.

# Upload my old notes to the app
In the app there's an option to restore data from backup. Backup is in sqlite3 format. In order to automatically upload my data to app I need to create a database file from my old notes.
First I need to fill in couple of workouts to see how the database with my inputs look like. Then I need to write python script that will convert my old notes into database.

Not convert them into database but make inserts into backup file.

## tasks
1. Get all rows from the DB that constitute one workout
1.a. Clean up data eg. Pull upy, Pull ups 
2. Based on 1. convert 1 workout from old notes into a series of inserts
3. Do it in a loop for every workout in the old notes
4. Test if updated DB file works in the App

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
- training_log,


Inserting 69 reps of excercise of id 100 on a given date
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
- pull ups (Pull up)
- pull ups + weight (Pull Up)
- neutral (Neutral Chin Up)
- muscle up (add Muscle Up into db)
- handstand pushups (Handstand Pushup)
- handstand pushups wall (Handstand Pushup Wall)
- handstand (Handstand)
- chin up (Chin Up)
- dips + weight (Chest Dip)
- przysiad (Barbell Squat)

## Info reagrding inserts into training_log table

### Workout comment
```sql
insert into WorkoutComment (date,comment)
values({date},{comment});
```
### Pull Up
```sql
insert into training_log (exercise_id,date,reps,metric_weight)
values(49,{date},{reps},{weight});
```
### Neutral Chin Up
```sql
insert into training_log (exercise_id,date,reps,metric_weight)
values(51,{date},{reps},{weight});
```
### Chin Up
```sql
insert into training_log (exercise_id,date,reps,metric_weight)
values(50,{date},{reps},{weight});
```
### Muscle Up
```sql
insert into training_log (exercise_id,date,reps,metric_weight)
values(toBeSeen,{date},{reps},{weight});
```
### Handstand Pushup
```sql
insert into training_log (exercise_id,date,reps,metric_weight)
values(108,{date},{reps},{weight});
```
### Handstand Pushup Wall
```sql
insert into training_log (exercise_id,date,reps,metric_weight)
values(100,{date},{reps},{weight});
```
### Handstand
```sql
insert into training_log (exercise_id,date,reps,metric_weight)
values(111,{date},{reps},{time});
```