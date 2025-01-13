import csv

# File paths
input_file = 'fon_fr_parallel_train.txt'  # Replace with your file path
output_file = 'fon_fr_parallel_train.csv'  # Replace with your desired output file path

# Open the input file and read its content
with open(input_file, 'r', encoding='utf-8-sig') as infile:
    lines = infile.readlines()

# Open the output file for writing
with open(output_file, 'w', newline='', encoding='utf-8-sig') as csvfile:
    writer = csv.writer(csvfile)
    
    # Write the header row
    writer.writerow(['Fon', 'French'])
    
    # Process each line
    for line in lines:
        # Split the line into Fon and French using tab as the delimiter
        parts = line.strip().split('\t')
        if len(parts) == 2:  # Ensure there are exactly two parts
            writer.writerow(parts)

print(f"CSV file has been created at {output_file}")
