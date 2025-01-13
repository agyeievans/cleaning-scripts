import os
import csv
import re

def natural_sort_key(s):
    # Function to help sort filenames naturally
    return [int(text) if text.isdigit() else text.lower()
            for text in re.split('([0-9]+)', s)]

def create_bilingual_csv(folder_path, output_csv):
    # Dictionary to store corresponding English and Yoruba texts
    paired_texts = {}
    
    # Get all files in the directory
    files = os.listdir(folder_path)
    
    # Sort files to ensure proper ordering
    files.sort(key=natural_sort_key)
    
    # Process English files and find their Yoruba counterparts
    for filename in files:
        if filename.startswith('en_'):
            # Get the corresponding Yoruba filename
            yoruba_file = 'yo_' + filename[3:]
            
            if yoruba_file in files:
                # Read English content
                with open(os.path.join(folder_path, filename), 'r', encoding='utf-8-sig') as en_file:
                    en_content = en_file.read().strip()
                
                # Read Yoruba content
                with open(os.path.join(folder_path, yoruba_file), 'r', encoding='utf-8-sig') as yo_file:
                    yo_content = yo_file.read().strip()
                
                # Store the pair using the file number as key
                file_number = filename[3:-4]  # Extract number from filename
                paired_texts[file_number] = (en_content, yo_content)
    
    # Write to CSV file
    with open(output_csv, 'w', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.writer(csvfile)
        # Write header
        writer.writerow(['English', 'Yoruba'])
        
        # Write content in order
        for number in sorted(paired_texts.keys(), key=int):
            writer.writerow(paired_texts[number])

# Example usage
folder_path = r'C:\Users\EVANS\Downloads\Compressed\en-tw.tmx\files'  # Current directory, modify as needed
output_csv = 'bilingual_texts.csv'

create_bilingual_csv(folder_path, output_csv)