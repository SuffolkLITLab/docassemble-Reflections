import csv
import sys

def create_reflection_yaml_from_csv(csv_file_path):
    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            week_number = row['Week']
            reflection_question = row['Reflection Question']
            create_reflection_yaml(week_number, reflection_question)

def create_reflection_yaml(week_number, reflection_question):
    yaml_content = f"""
---
include:
  - base_reflection.yml
---
metadata:
  title: |
    Weekly Reflection for Week {week_number}
---
sets: reflection_questions["chat"].initial_question
code: |
  reflection_questions["chat"].initial_question = '''
  {reflection_question}
  '''
---
id: first_page
continue button field: questions
question: |
  Weekly reflection
subquestion: |
  ${{ rubric_explanation }}
fields:
  - How was last week's class on a scale of 1 to 5?: reflection_questions["class_rating"]
    datatype: range
    min: 1
    max: 5
    step: 1
    default: 5
  - What do you think could be improved? What worked well?: reflection_questions["suggestions"]
    datatype: area
    rows: 3
    required: False
  - note: |
      ---
  - label: |
      ${{ reflection_questions["chat"].initial_question }}
    field: reflection_questions["chat"].initial_draft
    datatype: area
    rows: 5
    validate: |
      lambda y: (wc := len(y.split(" "))) > 50 or validation_error(f"Write at least 50 words (you wrote {{ wc }}).")
"""
    file_name = f"week_{week_number}.yml"
    with open(file_name, "w") as file:
        file.write(yaml_content)

    print(f"YAML file created: {file_name}")

if __name__ == "__main__":
    csv_file_path = sys.argv[1]
    create_reflection_yaml_from_csv(csv_file_path)
