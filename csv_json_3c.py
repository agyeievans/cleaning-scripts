import csv
import ast
import pandas as pd
from typing import List, Dict
import logging

def process_language_file(input_file: str, output_file: str) -> None:
    """
    Process a CSV file containing language data and separate it into columns.
    
    Args:
        input_file (str): Path to input CSV file
        output_file (str): Path to output CSV file
    """
    # Set up logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    try:
        # Read the input file with UTF-8-sig encoding to handle BOM
        rows: List[Dict] = []
        with open(input_file, 'r', encoding='utf-8-sig') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                try:
                    if row:  # Check if row is not empty
                        # Use ast.literal_eval to safely evaluate the string representation
                        # of the dictionary
                        data = ast.literal_eval(row[0])
                        rows.append({
                            'en': data.get('en', ''),
                            'eng': data.get('eng', ''),
                            'yor': data.get('yor', '')
                        })
                except (SyntaxError, ValueError) as e:
                    logger.error(f"Failed to parse row: {row}. Error: {str(e)}")
                    continue
                except IndexError as e:
                    logger.error(f"Empty or malformed row encountered. Error: {str(e)}")
                    continue
        
        # Convert to DataFrame
        df = pd.DataFrame(rows)
        
        # Save to CSV with UTF-8-sig encoding
        df.to_csv(output_file, index=False, encoding='utf-8-sig')
        logger.info(f"Successfully processed {len(rows)} rows and saved to {output_file}")
        
    except FileNotFoundError:
        logger.error(f"Input file {input_file} not found")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    # Example usage
    input_file = "train-00000-of-00001.csv"
    output_file = "train-00000-of-00001 2.csv"
    process_language_file(input_file, output_file)