import json
import csv
import sys

def json_to_csv(json_file, csv_file):
    try:
        # Read JSON file with UTF-8 encoding
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Open CSV file with UTF-8-sig encoding to handle special characters
        with open(csv_file, 'w', encoding='utf-8-sig', newline='') as f:
            writer = csv.writer(f)
            
            # Write header row
            writer.writerow(['instruction', 'input', 'output'])
            
            # Write data rows
            for item in data:
                writer.writerow([
                    item.get('instruction', ''),  # Using get() to handle missing keys
                    item.get('input', ''),
                    item.get('output', '')
                ])
                
        print(f"Successfully converted {json_file} to {csv_file}")
        
    except FileNotFoundError:
        print(f"Error: The file {json_file} was not found.")
    except json.JSONDecodeError:
        print(f"Error: {json_file} is not a valid JSON file.")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")

# Use the function
json_to_csv('alpaca_4k_lug.json', 'alpaca_4k_lug.csv')