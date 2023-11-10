import csv
import json

csv_filename = '/Users/mac/Downloads/Projects/eboard/data/primary_school/eboard_arithmetic.csv'
data = []

with open(csv_filename, 'r') as csv_file:
    reader = csv.DictReader(csv_file)
    for row in reader:
        data.append(row)
        
json_filename = '/Users/mac/Downloads/Projects/eboard/data/primary_school/eboard_arithmetic_lesson.json'

with open(json_filename, 'r') as json_file:
    lessons = json.load(json_file)
combined_data = {}
for item in data:
    topic_name = item['topic_name']
    if topic_name in lessons:
        lessons[topic_name].append(item)
    else:
        lessons[topic_name] = [item]

combined_json_data = json.dumps(lessons, ensure_ascii=False)
combined_json_filename = 'combined_data.json'

with open(combined_json_filename, 'w', encoding='utf-8') as combined_json_file:
    combined_json_file.write(combined_json_data)
