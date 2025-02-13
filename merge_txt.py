import csv

# Define file paths
file1_path = 'english.txt'
file2_path = 'twi.txt'
output_csv_path = 'bible english - twi.csv'

# Define column names
column1_name = 'English'
column2_name = 'Twi'

# Read lines from both files
with open(file1_path, 'r', encoding='utf-8-sig') as file1, open(file2_path, 'r', encoding='utf-8-sig') as file2:
    file1_lines = file1.readlines()
    file2_lines = file2.readlines()

# Ensure both files have the same number of lines
max_lines = max(len(file1_lines), len(file2_lines))
file1_lines.extend([''] * (max_lines - len(file1_lines)))  # Pad with empty strings if necessary
file2_lines.extend([''] * (max_lines - len(file2_lines)))  # Pad with empty strings if necessary

# Write to CSV
with open(output_csv_path, 'w', newline='', encoding='utf-8-sig') as csv_file:
    writer = csv.writer(csv_file)
    # Write header
    writer.writerow([column1_name, column2_name])
    # Write rows
    for line1, line2 in zip(file1_lines, file2_lines):
        writer.writerow([line1.strip(), line2.strip()])

print("Files merged successfully!")

output_csv_path
