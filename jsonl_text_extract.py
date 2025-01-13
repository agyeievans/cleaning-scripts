import json
import csv

def extract_texts_from_jsonl(input_jsonl_file, output_csv_file):
    """
    Extract texts from 'summary' and 'text' fields of a JSONL file and write to a CSV.
    
    Args:
    input_jsonl_file (str): Path to the input JSONL file
    output_csv_file (str): Path to the output CSV file
    """
    # Open the JSONL file for reading
    try:
        with open(input_jsonl_file, 'r', encoding='utf-8-sig') as jsonl_file, \
             open(output_csv_file, 'w', newline='', encoding='utf-8-sig') as csv_file:
            
            # Create a CSV writer
            csv_writer = csv.writer(csv_file)
            
            # Write header
            csv_writer.writerow(['Extracted Text'])
            
            # Read and process each line
            for line_number, line in enumerate(jsonl_file, 1):
                try:
                    # Parse each line as a JSON object
                    item = json.loads(line.strip())
                    
                    # Extract summary if it exists
                    if isinstance(item, dict):
                        if 'summary' in item:
                            csv_writer.writerow([item['summary']])
                        
                        # Extract text if it exists
                        if 'text' in item:
                            csv_writer.writerow([item['text']])
                    
                except json.JSONDecodeError:
                    print(f"Warning: Invalid JSON on line {line_number}. Skipping.")
                    continue
        
        print(f"CSV file '{output_csv_file}' has been created successfully.")
    
    except FileNotFoundError:
        print(f"Error: File {input_jsonl_file} not found")
    except PermissionError:
        print(f"Error: Permission denied when trying to read {input_jsonl_file} or write {output_csv_file}")

# Example usage
input_file = r'C:\Users\EVANS\Downloads\Compressed\en-tw.tmx\yoruba_val.jsonl'  # Replace with your .jsonl file path
output_file = 'yoruba_val.csv'  # Replace with desired output file path

extract_texts_from_jsonl(input_file, output_file)