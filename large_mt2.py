import pandas as pd
import os
from typing import List, Tuple
import logging

def setup_logging():
    """Configure logging for the script"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def get_language_pairs() -> List[Tuple[str, str]]:
    """Return all possible language pair combinations"""
    languages = ['en', 'yo', 'ig', 'ha', 'hau', 'igbo']
    pairs = []
    for source in languages:
        for target in languages:
            if source != target:
                pairs.append((source, target))
    return pairs

def get_full_language_name(code: str) -> str:
    """Convert language code to full name"""
    language_map = {
        'en': 'english',
        'yo': 'yoruba',
        'ig': 'igbo',
        'ha': 'hausa',
        'hau': 'hausa',
        'igbo': 'igbo',
    }
    return language_map.get(code, code).title()

def create_output_directory(output_dir: str):
    """Create output directory if it doesn't exist"""
    try:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            logging.info(f"Created output directory: {output_dir}")
    except Exception as e:
        logging.error(f"Error creating output directory: {e}")
        raise

def separate_language_pairs(input_file: str, output_dir: str = 'language_pairs'):
    """
    Separate CSV file into multiple files based on language pairs
    
    Args:
        input_file (str): Path to input CSV file
        output_dir (str): Directory to store output files
    """
    try:
        # Set up logging
        setup_logging()
        
        # Create output directory
        create_output_directory(output_dir)
        
        # Get base filename without extension
        base_filename = os.path.splitext(os.path.basename(input_file))[0]
        
        # Read the CSV file with UTF-8 encoding
        logging.info(f"Reading input file: {input_file}")
        df = pd.read_csv(input_file, encoding='utf-8')
        
        # Validate required columns
        required_columns = ['source_text', 'target_text', 'source_language', 'target_language']
        if not all(col in df.columns for col in required_columns):
            raise ValueError(f"CSV must contain all required columns: {required_columns}")
        
        # Get all language pairs
        language_pairs = get_language_pairs()
        
        # Process each language pair
        for source_lang, target_lang in language_pairs:
            try:
                # Filter data for current language pair
                mask = (df['source_language'] == source_lang) & (df['target_language'] == target_lang)
                pair_df = df[mask]
                
                # Skip if no data for this language pair
                if pair_df.empty:
                    logging.info(f"No data found for language pair {source_lang}-{target_lang}")
                    continue
                
                # Select only source_text and target_text columns
                pair_df = pair_df[['source_text', 'target_text']]
                
                # Rename columns to full language names
                pair_df.columns = [
                    get_full_language_name(source_lang),
                    get_full_language_name(target_lang)
                ]
                
                # Create output filename with new naming pattern
                output_file = os.path.join(output_dir, f'{base_filename} {source_lang}-{target_lang}.csv')
                
                # Save to CSV with UTF-8-SIG encoding
                pair_df.to_csv(output_file, encoding='utf-8-sig', index=False)
                logging.info(f"Created file for {source_lang}-{target_lang} with {len(pair_df)} rows: {output_file}")
                
            except Exception as e:
                logging.error(f"Error processing language pair {source_lang}-{target_lang}: {e}")
                continue
                
    except Exception as e:
        logging.error(f"Error processing file: {e}")
        raise

if __name__ == "__main__":
    try:
        input_file = "train-00000-of-00001.csv"  # Replace with your input file path
        separate_language_pairs(input_file)
    except Exception as e:
        logging.error(f"Script execution failed: {e}")