import json
import csv
from pathlib import Path
from typing import Dict, List, Tuple
from tqdm import tqdm

# Specify your input and output file paths here
INPUT_FILE = "train.jsonl"  # Change this to your JSONL file path
OUTPUT_FILE = "train.csv"   # Change this to your desired output CSV file path

def process_jsonl_file(input_file: str) -> List[Tuple[str, str]]:
    """
    Process the JSONL file and extract Yoruba-English pairs.
    
    Args:
        input_file (str): Path to the input JSONL file
        
    Returns:
        List[Tuple[str, str]]: List of (Yoruba, English) translation pairs
    """
    translations = []
    total_lines = sum(1 for _ in open(input_file, 'r', encoding='utf-8'))
    
    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            for line in tqdm(file, total=total_lines, desc="Processing translations"):
                try:
                    data = json.loads(line.strip())
                    if isinstance(data, dict) and 'yoruba' in data and 'english' in data:
                        translations.append((data['yoruba'], data['english']))
                    else:
                        print(f"Warning: Skipping malformed line: {line.strip()}")
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON line: {str(e)}")
                    continue
    except FileNotFoundError:
        raise FileNotFoundError(f"Input file '{input_file}' not found")
    except Exception as e:
        raise Exception(f"Error reading input file: {str(e)}")
    
    return translations

def save_to_csv(translations: List[Tuple[str, str]], output_file: str) -> None:
    """
    Save translations to a CSV file with UTF-8-SIG encoding.
    
    Args:
        translations (List[Tuple[str, str]]): List of (Yoruba, English) translation pairs
        output_file (str): Path to the output CSV file
    """
    try:
        with open(output_file, 'w', encoding='utf-8-sig', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Yoruba', 'English'])  # Write header
            
            for yoruba, english in tqdm(translations, desc="Saving to CSV"):
                writer.writerow([yoruba, english])
                
        print(f"\nSuccessfully saved {len(translations)} translations to {output_file}")
    except Exception as e:
        raise Exception(f"Error saving to CSV: {str(e)}")

def main():
    try:
        print(f"Processing file: {INPUT_FILE}")
        translations = process_jsonl_file(INPUT_FILE)
        if not translations:
            print("No valid translations found in the input file")
            return
            
        save_to_csv(translations, OUTPUT_FILE)
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()