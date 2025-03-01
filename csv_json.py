import pandas as pd
import ast

# Define file path
file_path = "nllb-lug-en-vigorous-clean.csv"  # Change this to your actual file path
output_path = "nllb-lug-en-vigorous-clean 2.csv"  # Change this to your desired output path

# Load the CSV file
df = pd.read_csv(file_path, encoding="utf-8-sig")

# Convert the single column to a list of dictionaries
df = df.iloc[:, 0].apply(ast.literal_eval)

# Normalize the dictionary into separate columns
df = pd.json_normalize(df)

# Keep only 'eng' and 'yor' columns, rename them
if "eng_Latn" in df.columns and "lug_Latn" in df.columns:
    df = df.rename(columns={"eng_Latn": "English", "lug_Latn": "Luganda"})
    df = df[["English", "Luganda"]]
else:
    raise ValueError("The expected columns ('eng' and 'yor') are missing from the input data.")

# Save the processed file
df.to_csv(output_path, encoding="utf-8-sig", index=False)

print(f"Processed file saved to: {output_path}")
