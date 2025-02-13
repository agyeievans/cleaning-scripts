import pandas as pd

# Load the input CSV file
input_file = "Train.csv"
data = pd.read_csv(input_file, encoding="utf-8-sig")

# Separate the data into two DataFrames: one for French and Fon, one for French and Ewe
fon_data = data[data['Target_Language'] == 'Fon'][['French', 'Target']]
ewe_data = data[data['Target_Language'] == 'Ewe'][['French', 'Target']]

# Rename the columns to match the output requirements
fon_data.columns = ['French', 'Fon']
ewe_data.columns = ['French', 'Ewe']

# Save the separated data to new CSV files
fon_output_file = "French_Fon.csv"
ewe_output_file = "French_Ewe.csv"

fon_data.to_csv(fon_output_file, index=False, encoding="utf-8-sig")
ewe_data.to_csv(ewe_output_file, index=False, encoding="utf-8-sig")

print(f"French-Fon data saved to: {fon_output_file}")
print(f"French-Ewe data saved to: {ewe_output_file}")
