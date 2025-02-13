import json
import csv
import sys
from typing import List, Dict
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def read_json_file(file_path: str) -> List[Dict]:
    """
    Read and parse the JSON file.
    
    Args:
        file_path (str): Path to the JSON file
        
    Returns:
        List[Dict]: Parsed JSON data
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        logging.error(f"Error: File '{file_path}' not found")
        sys.exit(1)
    except json.JSONDecodeError:
        logging.error("Error: Invalid JSON format in the input file")
        sys.exit(1)
    except Exception as e:
        logging.error(f"Unexpected error reading file: {str(e)}")
        sys.exit(1)

def extract_translations(data: List[Dict]) -> List[Dict[str, str]]:
    """
    Extract English and Luganda translations from the data.
    
    Args:
        data (List[Dict]): The parsed JSON data
        
    Returns:
        List[Dict[str, str]]: List of translation pairs
    """
    translations = []
    for item in data:
        try:
            translation = item.get('translation', {})
            en = translation.get('en', '')
            lg = translation.get('lg', '')
            
            if en and lg:  # Only add if both translations exist
                translations.append({
                    'English': en,
                    'Luganda': lg
                })
            else:
                logging.warning(f"Skipping entry with ID {item.get('id', 'unknown')}: Missing translation")
        except Exception as e:
            logging.warning(f"Error processing entry: {str(e)}")
            continue
    
    return translations

def write_csv_file(translations: List[Dict[str, str]], output_file: str):
    """
    Write translations to a CSV file with UTF-8-sig encoding.
    
    Args:
        translations (List[Dict[str, str]]): List of translation pairs
        output_file (str): Path to the output CSV file
    """
    try:
        with open(output_file, 'w', encoding='utf-8-sig', newline='') as file:
            if not translations:
                logging.warning("No translations to write")
                return
                
            writer = csv.DictWriter(file, fieldnames=['English', 'Luganda'])
            writer.writeheader()
            writer.writerows(translations)
            logging.info(f"Successfully wrote {len(translations)} translations to {output_file}")
    except Exception as e:
        logging.error(f"Error writing CSV file: {str(e)}")
        sys.exit(1)

def main():
    input_file = 'luganda_to_english.json'  # Change this to your input file path
    output_file = 'luganda_to_english.csv'  # Change this to your desired output file path
    
    try:
        # Read and process the data
        json_data = read_json_file(input_file)
        translations = extract_translations(json_data)
        write_csv_file(translations, output_file)
        
    except Exception as e:
        logging.error(f"Program failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()