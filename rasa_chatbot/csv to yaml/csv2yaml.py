import csv
import yaml

# Open the CSV file and read the contents with explicit encoding (e.g., utf-8)
with open('data.csv', 'r', encoding='utf-8') as csv_file:
    csv_reader = csv.reader(csv_file)

    # Create an empty list to store the data
    data = []

    # Iterate over the rows of the CSV file and append each row to the data list
    for row in csv_reader:
        data.append(row)

# Open the YAML file and write the data
with open('data.yaml', 'w', encoding='utf-8') as yaml_file:
    yaml.dump(data, yaml_file)
