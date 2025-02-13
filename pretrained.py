import pandas as pd
import os
import logging
from typing import Dict, Set

def separate_languages(input_file: str) -> None:
    """
    Process a CSV file and separate contents by language into different files.
    
    Args:
        input_file (str): Path to input CSV file
    """
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)
    
    try:
        # Read the CSV file with UTF-8-sig encoding
        df = pd.read_csv(input_file, encoding='utf-8-sig')
        
        # Get the base filename without extension
        base_filename = os.path.splitext(input_file)[0]
        
        # Dictionary to store texts by language
        language_texts: Dict[str, list] = {}
        
        # Process each row
        for _, row in df.iterrows():
            try:
                text = row['text']
                lang = row['language']
                
                if lang not in language_texts:
                    language_texts[lang] = []
                    
                language_texts[lang].append(text)
                
            except KeyError as e:
                logger.error(f"Missing required column: {str(e)}")
                continue
            except Exception as e:
                logger.error(f"Error processing row: {str(e)}")
                continue
        
        # Create separate files for each language
        for lang, texts in language_texts.items():
            try:
                output_filename = f"{base_filename} {lang}.csv"
                
                # Create DataFrame with just the texts
                output_df = pd.DataFrame(texts, columns=['text'])
                
                # Save to CSV with UTF-8-sig encoding
                output_df.to_csv(
                    output_filename,
                    index=False,
                    encoding='utf-8-sig',
                    quoting=1  # Quote all fields
                )
                
                logger.info(f"Created {output_filename} with {len(texts)} entries")
                
            except Exception as e:
                logger.error(f"Error saving file for language {lang}: {str(e)}")
                continue
                
        logger.info(f"Processing complete. Created files for {len(language_texts)} languages")
        
    except FileNotFoundError:
        logger.error(f"Input file {input_file} not found")
    except pd.errors.EmptyDataError:
        logger.error(f"The file {input_file} is empty")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    # Example usage
    input_file = "train-00000-of-00001.csv"
    separate_languages(input_file)