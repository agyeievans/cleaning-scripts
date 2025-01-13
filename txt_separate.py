# import csv

# # File paths
# input_file = 'eng.lug.txt'  # Replace with your file path
# output_file = 'eng.lug.csv'  # Replace with your desired output file path

# # Open the input file and read its content
# with open(input_file, 'r', encoding='utf-8') as infile:
#     lines = infile.readlines()

# # Open the output file for writing
# with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
#     writer = csv.writer(csvfile)
    
#     # Write the header row
#     writer.writerow(['English', 'Luganda'])
    
#     # Process each line
#     for line in lines:
#         # Split the line into Fon and French using tab as the delimiter
#         parts = line.strip().split('\t')
#         if len(parts) == 2:  # Ensure there are exactly two parts
#             writer.writerow(parts)

# print(f"CSV file has been created at {output_file}")

# import csv

# # File paths
# input_file = 'eng.lug.txt'  # Replace with your file path
# output_file = 'eng.lug.csv'  # Replace with your desired output file path

# # Open the input file with proper encoding
# with open(input_file, 'r', encoding='utf-8-sig') as infile:
#     lines = infile.readlines()

# # Open the output file for writing
# with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
#     writer = csv.writer(csvfile)
    
#     # Write the header row
#     writer.writerow(['English', 'Luganda'])
    
#     # Process each line
#     for line in lines:
#         # Split the line into Fon and French using tab as the delimiter
#         parts = line.strip().split('\t')
#         if len(parts) == 2:  # Ensure there are exactly two parts
#             writer.writerow(parts)

# print(f"CSV file has been created at {output_file}")


# import chardet

# input_file = 'eng.lug.txt'

# with open(input_file, 'rb') as f:
#     result = chardet.detect(f.read())
#     print(result)

import csv

# File paths
input_file = 'en_fon_parallel_train.txt'  # Replace with your file path
output_file = 'en_fon_parallel_train.csv'  # Replace with your desired output file path

# Open the input file with the correct encoding
with open(input_file, 'r', encoding='utf-8') as infile:  # Replace 'utf-16' with the detected encoding
    lines = infile.readlines()

# Open the output file for writing
with open(output_file, 'w', newline='', encoding='utf-8-sig') as csvfile:
    writer = csv.writer(csvfile)
    
    # Write the header row
    writer.writerow(['English','Fon'])
    
    # Process each line
    for line in lines:
        # Split the line into Fon and French using tab as the delimiter
        parts = line.strip().split('\t')
        if len(parts) == 2:  # Ensure there are exactly two parts
            writer.writerow(parts)

print(f"CSV file has been created at {output_file}")

