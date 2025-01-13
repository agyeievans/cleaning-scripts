import csv

# Define file paths
file1_path = 'Autshumato.BilingualCorpus(English-Afrikaans).v2.0.en.txt'
file2_path = 'Autshumato.BilingualCorpus(English-Afrikaans).v2.0.af.txt'
output_csv_base = 'Autshumato BilingualCorpus English-Afrikaans'  # Base name for CSV files

# Define column names
column1_name = 'English'
column2_name = 'Afrikaans'

# Maximum rows per CSV file
max_rows_per_file = 1_000_000

# Read lines from both files
with open(file1_path, 'r', encoding='utf-8-sig') as file1, open(file2_path, 'r', encoding='utf-8-sig') as file2:
    file1_lines = file1.readlines()
    file2_lines = file2.readlines()

# Ensure both files have the same number of lines
max_lines = max(len(file1_lines), len(file2_lines))
file1_lines.extend([''] * (max_lines - len(file1_lines)))  # Pad with empty strings if necessary
file2_lines.extend([''] * (max_lines - len(file2_lines)))  # Pad with empty strings if necessary

# Write to multiple CSVs
file_count = 1
row_count = 0
csv_file = open(f"{output_csv_base}_{file_count}.csv", 'w', newline='', encoding='utf-8-sig')
writer = csv.writer(csv_file)
writer.writerow([column1_name, column2_name])  # Write header

for line1, line2 in zip(file1_lines, file2_lines):
    if row_count >= max_rows_per_file:
        # Close current file and start a new one
        csv_file.close()
        file_count += 1
        row_count = 0
        csv_file = open(f"{output_csv_base}_{file_count}.csv", 'w', newline='', encoding='utf-8-sig')
        writer = csv.writer(csv_file)
        writer.writerow([column1_name, column2_name])  # Write header

    # Write row
    writer.writerow([line1.strip(), line2.strip()])
    row_count += 1

# Close the last file
csv_file.close()
