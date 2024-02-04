import csv
import yaml

# Open the CSV file and read the contents with explicit encoding (e.g., utf-8)
with open('data.csv', 'r', encoding='utf-8') as csv_file:
    csv_reader = csv.DictReader(csv_file)

    # Create an empty list to store the 'law' column data
    law_column_data = []

    # Iterate over the rows of the CSV file and extract the 'law' column
    for row in csv_reader:
        # Assuming 'law' is the header of the column you want
        law_column_data.append(row['Law'])

# Open the YAML file and write the 'law' column data
with open('law_data.yaml', 'w', encoding='utf-8') as yaml_file:
    yaml.dump(law_column_data, yaml_file)
