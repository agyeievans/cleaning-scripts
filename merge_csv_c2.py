import pandas as pd

# Load the CSV files with utf-8-sig encoding
file_english = 'train english.csv'
file_arabic = 'train arabic.csv'

# Read each CSV file into a DataFrame
df_english = pd.read_csv(file_english, encoding='utf-8-sig')
df_arabic = pd.read_csv(file_arabic, encoding='utf-8-sig')

# Extract the first columns from each file and create a new DataFrame with them
df_first_columns = pd.DataFrame({
    'English': df_english.iloc[:, 0],  # First column from English file
    'Arabic': df_arabic.iloc[:, 0]     # First column from Arabic file
})

# Extract the second columns from each file and create another DataFrame with them
df_second_columns = pd.DataFrame({
    'English': df_english.iloc[:, 1],  # Second column from English file
    'Arabic': df_arabic.iloc[:, 1]     # Second column from Arabic file
})

# Save the new DataFrames to CSV files with utf-8-sig encoding
output_file_first_columns = 'train combined_first_columns.csv'
output_file_second_columns = 'train combined_second_columns.csv'

df_first_columns.to_csv(output_file_first_columns, index=False, encoding='utf-8-sig')
df_second_columns.to_csv(output_file_second_columns, index=False, encoding='utf-8-sig')

output_file_first_columns, output_file_second_columns
