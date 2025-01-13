import json
import csv

def convert_json_to_csv(input_json_file, output_csv_file):
    """
    Convert a JSON file to a CSV file with robust error handling.
    
    Args:
    input_json_file (str): Path to the input JSON file
    output_csv_file (str): Path to the output CSV file
    """
    # Read the JSON file
    with open(input_json_file, 'r', encoding='utf-8-sig') as json_file:
        # Try different parsing methods
        try:
            # First, try parsing as a list of dictionaries
            data = json.load(json_file)
        except json.JSONDecodeError:
            # If that fails, reset file pointer and try reading as text
            json_file.seek(0)
            data_text = json_file.read().strip()
            
            # Try parsing text variations
            if data_text.startswith('[') and data_text.endswith(']'):
                data = json.loads(data_text)
            elif data_text.startswith('{') and data_text.endswith('}'):
                data = [json.loads(data_text)]
            else:
                raise ValueError("Unable to parse JSON file")
    
    # Open the CSV file for writing
    with open(output_csv_file, 'w', newline='', encoding='utf-8-sig') as csv_file:
        # Create a CSV writer
        csv_writer = csv.writer(csv_file)
        
        # Write the header
        csv_writer.writerow(['French', 'Mossi'])
        
        # Handle different possible data structures
        if isinstance(data, dict):
            # If it's a single dictionary
            for key, value in data.items():
                if isinstance(value, dict) and 'fr' in value and 'mos' in value:
                    csv_writer.writerow([value['fr'], value['mos']])
        elif isinstance(data, list):
            # If it's a list of dictionaries
            for item in data:
                # Additional error handling for different possible structures
                if isinstance(item, dict):
                    # Try accessing keys with different variations
                    fr = item.get('fr') or item.get('Fr') or item.get('FR') or ''
                    en = item.get('mos') or item.get('Mos') or item.get('MOS') or ''
                    csv_writer.writerow([fr, en])
                elif isinstance(item, str):
                    # If item is a string, split it or handle accordingly
                    parts = item.split(',')
                    if len(parts) >= 2:
                        csv_writer.writerow(parts[:2])
        
    print(f"CSV file '{output_csv_file}' has been created successfully.")

# Example usage
input_file = r'C:\Users\EVANS\Downloads\Compressed\en-tw.tmx\dev.json'  # Replace with your actual JSON file path
output_file = 'output.csv'  # Replace with desired output file path

convert_json_to_csv(input_file, output_file)