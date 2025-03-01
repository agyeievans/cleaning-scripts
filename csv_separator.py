import csv
import os
import re
from tqdm import tqdm
import pandas as pd

# === CONFIGURATION SETTINGS ===
# Set your input file path here
INPUT_FILE_PATH = "salt-m2e-15-3-instruction-validation.csv"
# Set your output directory here (leave as None to use the same directory as the input file)
OUTPUT_DIRECTORY = None
# === END CONFIGURATION ===

def extract_language(instruction):
    """Extract source language from instruction string."""
    match = re.search(r'Translate from (\w+) to', instruction)
    if match:
        return match.group(1)
    return None

def separate_by_language(input_file, output_dir=None):
    """
    Separate CSV file into multiple files by language.
    
    Args:
        input_file (str): Path to input CSV file
        output_dir (str, optional): Directory to save output files
    
    Returns:
        dict: Dictionary mapping languages to output file paths
    """
    if output_dir is None:
        output_dir = os.path.dirname(input_file) or '.'
    
    os.makedirs(output_dir, exist_ok=True)
    
    # Get base filename without extension
    base_filename = os.path.splitext(os.path.basename(input_file))[0]
    
    # Dictionary to hold rows for each language
    rows_by_language = {}
    
    # First pass: count rows to set up progress bar
    print(f"Counting rows in {input_file}...")
    try:
        total_rows = sum(1 for _ in open(input_file, 'r', encoding='utf-8'))
        total_rows -= 1  # Subtract header row
    except Exception as e:
        print(f"Error counting rows: {e}")
        total_rows = 0
    
    # Second pass: process rows
    print(f"Processing {total_rows} rows...")
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            # Print found columns for debugging
            print(f"Found columns: {reader.fieldnames}")
            
            # Handle BOM character in column names
            fixed_fieldnames = [name.replace('\ufeff', '') for name in reader.fieldnames]
            expected_columns = ['input', 'output', 'instruction']
            
            # Check if fixed column names match expected columns
            if not all(col in fixed_fieldnames for col in expected_columns):
                raise ValueError(f"CSV must contain columns: {', '.join(expected_columns)}")
            
            for row in tqdm(reader, total=total_rows):
                # Create a new row with fixed column names
                fixed_row = {}
                for key, value in row.items():
                    fixed_key = key.replace('\ufeff', '')
                    fixed_row[fixed_key] = value
                
                instruction = fixed_row.get('instruction', '')
                
                language = extract_language(instruction)
                if not language:
                    print(f"Warning: Could not extract language from instruction: '{instruction}'")
                    continue
                
                # Store rows by language
                if language not in rows_by_language:
                    rows_by_language[language] = []
                rows_by_language[language].append(fixed_row)
    
    except Exception as e:
        print(f"Error reading input file: {e}")
        return {}
    
    # Write language-specific files
    print(f"Writing files for {len(rows_by_language)} languages...")
    language_files = {}
    
    for language, rows in rows_by_language.items():
        try:
            output_file = os.path.join(output_dir, f"{base_filename} {language} to English.csv")
            
            # Write to CSV using pandas for better handling of special characters
            df = pd.DataFrame(rows)
            df.to_csv(output_file, index=False, quoting=csv.QUOTE_NONNUMERIC)
            
            print(f"Created {output_file} with {len(rows)} rows")
            language_files[language] = output_file
        
        except Exception as e:
            print(f"Error writing file for {language}: {e}")
    
    return language_files

def main():
    """Main function to run the script."""
    print(f"Starting to process {INPUT_FILE_PATH}")
    
    # Verify the input file exists
    if not os.path.exists(INPUT_FILE_PATH):
        print(f"Error: The file {INPUT_FILE_PATH} does not exist.")
        return
    
    result = separate_by_language(INPUT_FILE_PATH, OUTPUT_DIRECTORY)
    
    if result:
        print(f"Successfully created {len(result)} files:")
        for language, filepath in result.items():
            print(f"  - {language}: {filepath}")
    else:
        print("No files were created.")

if __name__ == "__main__":
    main()