import re

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

# Print or use the split entries as needed
for entry in exercise_entries:
    print(entry)
    print("------------")
