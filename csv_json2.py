import csv
import json
import re
import os
from tqdm import tqdm

def process_csv(input_file, output_file):
    """
    Process the CSV file by extracting English and Luganda text from each row
    and saving them as separate columns in a new CSV file.
    
    Args:
        input_file: Path to the input CSV file
        output_file: Path to the output CSV file
    """
    try:
        # Get total row count for progress tracking
        total_rows = sum(1 for _ in open(input_file, 'r', encoding='utf-8-sig'))
        
        # Open the input and output files
        with open(input_file, 'r', encoding='utf-8-sig') as infile, \
             open(output_file, 'w', encoding='utf-8-sig', newline='') as outfile:
            
            reader = csv.reader(infile)
            writer = csv.writer(outfile)
            
            # Write header row
            writer.writerow(['English', 'Luganda'])
            
            # Process each row with progress bar
            for i, row in enumerate(tqdm(reader, total=total_rows, desc="Processing rows")):
                try:
                    if not row:  # Skip empty rows
                        continue
                        
                    # Get the first column which contains our data
                    data_str = row[0]
                    
                    # Using a more robust regex pattern
                    pattern = r"'eng_Latn':\s*(.*?),\s*'lug_Latn':\s*(.*?)}$"
                    match = re.search(pattern, data_str)
                    
                    if match:
                        english = match.group(1).strip()
                        luganda = match.group(2).strip()
                        
                        # Remove any leading/trailing quotes if they exist
                        if english.startswith('"') and english.endswith('"'):
                            english = english[1:-1]
                        
                        if luganda.startswith('"') and luganda.endswith('"'):
                            luganda = luganda[1:-1]
                        
                        # Write to the output file
                        writer.writerow([english, luganda])
                    else:
                        # If the standard pattern doesn't work, try an alternative approach
                        # Split the string by 'lug_Latn'
                        parts = data_str.split("'lug_Latn':")
                        if len(parts) == 2:
                            # Extract English part
                            eng_part = parts[0]
                            eng_match = re.search(r"'eng_Latn':\s*(.*?)$", eng_part)
                            
                            # Extract Luganda part
                            lug_part = parts[1].strip()
                            if lug_part.endswith('}'):
                                lug_part = lug_part[:-1]
                            
                            if eng_match:
                                english = eng_match.group(1).strip()
                                if english.endswith(','):
                                    english = english[:-1].strip()
                                
                                if english.startswith('"') and english.endswith('"'):
                                    english = english[1:-1]
                                
                                if lug_part.startswith('"') and lug_part.endswith('"'):
                                    lug_part = lug_part[1:-1]
                                
                                writer.writerow([english, lug_part])
                            else:
                                print(f"Could not extract data from row {i+1}: {data_str}")
                        else:
                            print(f"Could not extract data from row {i+1}: {data_str}")
                    
                except Exception as e:
                    print(f"Error processing row {i+1}: {e}")
                    continue
        
        print(f"Processing complete. Output saved to {output_file}")
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    input_file = "nllb-lug-en-vigorous-clean.csv"
    output_file = "nllb-lug-en-vigorous-clean 2.csv"
    process_csv(input_file, output_file)
