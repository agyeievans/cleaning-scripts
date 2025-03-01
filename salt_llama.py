import re
import csv
import os
from tqdm import tqdm

def process_translation_data(input_file, output_file):
    """
    Process the translation data file, extracting Lugbara and English translations,
    and save them to a CSV file.
    
    Args:
        input_file (str): Path to the input file
        output_file (str): Path to the output CSV file
    """
    print(f"Processing file: {input_file}")
    print(f"Output will be saved to: {output_file}")
    
    # Regular expression to extract the translation pairs
    pattern = r'<s>\[INST\] Translate lgg to eng: (.*?) \[/INST\] (.*?) </s>'
    
    try:
        # Read the input file
        with open(input_file, 'r', encoding='utf-8-sig') as f:
            content = f.read()
        
        # Extract all matches
        matches = re.findall(pattern, content)
        total_matches = len(matches)
        print(f"Found {total_matches} translation pairs")
        
        # Write the translations to a CSV file
        with open(output_file, 'w', encoding='utf-8-sig', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Lugbara', 'English'])  # Write header
            
            # Process each match with a progress bar
            for lgg, eng in tqdm(matches, desc="Processing translations"):
                writer.writerow([lgg.strip(), eng.strip()])
        
        print(f"Successfully processed {total_matches} translation pairs.")
        print(f"Output saved to: {output_file}")
        
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
    except PermissionError:
        print(f"Error: Permission denied when trying to access '{input_file}' or write to '{output_file}'.")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    # Set simple file names - files should be in the same directory as the script
    input_file = "train-salt-llama-lgg-to-eng.csv"
    output_file = "train-salt-llama-lgg-to-eng 2.csv"
    
    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"Warning: Input file not found at {input_file}")
        print("Please make sure the input file is in the same directory as this script")
        print("or enter the correct path below")
        input_file = input("Enter the file name or full path to the input file: ")
    
    # Process the translations
    process_translation_data(input_file, output_file)