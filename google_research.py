import csv
import pandas as pd

# Read the TSV file
df = pd.read_csv('zul_mono.tsv', sep='\t', encoding='utf-8', header=None)

# Rename the columns
df.columns = ['Zulu']

# df.columns = ['Column 1', 'Column 2', 'Column 3', 'Column 4', 'Column 5', 'Column 6', 'Column 7', 'Column 8', 'Column 9', 'Column 10', 'Column 11', 'Column 12']

# Write to CSV with utf-8-sig encoding
df.to_csv('zul_mono.csv', encoding='utf-8-sig', index=False)

print("Conversion completed successfully!")


# import pandas as pd

# # Load the file with error handling for inconsistent rows
# file_path = "health_test_data.csv"  # Replace with your file path

# try:
#     # Read the file, skipping problematic lines
#     data = pd.read_csv(
#         file_path, 
#         delimiter="\t", 
#         header=None, 
#         on_bad_lines="skip"  # Skips bad lines
#     )
#     print("File loaded successfully!")
# except pd.errors.ParserError as e:
#     print("Error loading the file:", e)

# # Assign the column names if the data is loaded successfully
# if 'data' in locals():
#     column_names = [
#         "image", "english", "audio_id", "nyanja", "BitsPerSample",
#         "durationMsec", "sampleRate", "speaker_gender", 
#         "speaker_birth_year", "speaker_name", "mother_tongue", "extra_column", "extra_column2"
#     ]

#     if len(data.columns) >= len(column_names):  # Ensure enough columns exist
#         data.columns = column_names[:len(data.columns)]
#         # Save the processed file
#         output_path = "processed data.csv"  # Replace with your desired output file path
#         data.to_csv(output_path, index=False)
#         print("File processed and saved as:", output_path)
#     else:
#         print("The data does not have enough columns for renaming.")
# import pandas as pd

# # Load the file with error handling for inconsistent rows
# file_path = "health_test_data.csv"  # Replace with your file path

# try:
#     # Read the file, skipping problematic lines
#     data = pd.read_csv(
#         file_path, 
#         delimiter="\t", 
#         header=None, 
#         on_bad_lines="skip"  # Skips bad lines
#     )
#     print("File loaded successfully!")
# except pd.errors.ParserError as e:
#     print("Error loading the file:", e)

# # Assign the column names if the data is loaded successfully
# if 'data' in locals():
#     column_names = [
#         "image", "english", "audio_id", "nyanja", "BitsPerSample",
#         "durationMsec", "sampleRate", "speaker_gender", 
#         "speaker_birth_year", "speaker_name", "mother_tongue", "extra_column",
#     ]

#     if len(data.columns) >= len(column_names):  # Ensure enough columns exist
#         data.columns = column_names[:len(data.columns)]
#         # Save the processed file
#         output_path = "processed data.csv"  # Replace with your desired output file path
#         data.to_csv(output_path, index=False)
#         print("File processed and saved as:", output_path)
#     else:
#         print("The data does not have enough columns for renaming.")
