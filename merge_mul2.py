import os
import csv

def convert_to_bilingual_csv(english_files):
 
    for english_file_path in english_files:
        # Determine the corresponding Nyanya file path
        base_name = os.path.basename(english_file_path)
        nyanya_file_path = english_file_path.replace('_en.txt', '_ny.txt')
        
        # Output CSV file will have the same base name but with .csv extension
        output_csv_path = os.path.splitext(english_file_path)[0] + '.csv'
        
        # Read both files
        try:
            with open(english_file_path, 'r', encoding='utf-8-sig') as en_file, \
                 open(nyanya_file_path, 'r', encoding='utf-8-sig') as ny_file, \
                 open(output_csv_path, 'w', encoding='utf-8-sig', newline='') as csv_file:
                
                # Create CSV writer
                csv_writer = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
                
                # Write header
                csv_writer.writerow(['English', 'Nyanya'])
                
                # Read and write lines
                for en_line, ny_line in zip(en_file, ny_file):
                    # Strip whitespace and remove newline characters
                    en_line = en_line.strip()
                    ny_line = ny_line.strip()
                    
                    # Write to CSV
                    csv_writer.writerow([en_line, ny_line])
                
                print(f"Converted {base_name} to {os.path.basename(output_csv_path)}")
        
        except FileNotFoundError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Unexpected error processing {base_name}: {e}")

def main():
    # Current directory
    current_dir = os.getcwd()
    
    # Find all English files
    english_files = [
        os.path.join(current_dir, f) 
        for f in os.listdir(current_dir) 
        if f.endswith('_en.txt')
    ]
    
    # Sort files to ensure consistent processing
    english_files.sort()
    
    # Convert files
    convert_to_bilingual_csv(english_files)

if __name__ == "__main__":
    main()