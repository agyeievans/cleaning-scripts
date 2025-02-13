import pandas as pd
import os

def create_language_pairs(input_file, output_dir='output'):
    """
    Creates separate CSV files for English paired with each African language.
    
    Args:
        input_file (str): Path to the input CSV file
        output_dir (str): Directory to save the output files (default: 'output')
    """
    try:
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Read the CSV file
        df = pd.read_csv(input_file)
        
        # Verify that all expected columns are present
        expected_columns = ['eng', 'lug', 'ach', 'teo', 'lgg', 'nyn']
        missing_columns = [col for col in expected_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"Missing columns: {', '.join(missing_columns)}")
        
        # Dictionary of language codes to full names
        language_names = {
            'lug': 'Luganda',
            'ach': 'Acholi',
            'teo': 'Ateso',
            'lgg': 'Lugbara',
            'nyn': 'Nyankore'
        }
        
        # Create separate CSV files for each language pair
        for lang_code, lang_name in language_names.items():
            # Create a new dataframe with just English and the target language
            paired_df = df[['eng', lang_code]].copy()
            
            # Rename columns to be more descriptive
            paired_df.columns = ['English', lang_name]
            
            # Verify no missing values
            if paired_df.isna().any().any():
                print(f"Warning: Found missing values in {lang_name} pair")
            
            # Create output filename
            output_file = os.path.join(output_dir, f'english_{lang_code.lower()}.csv')
            
            # Save to CSV with UTF-8-SIG encoding
            paired_df.to_csv(output_file, index=False, encoding='utf-8-sig')
            print(f"Created {output_file}")

    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found")
    except pd.errors.EmptyDataError:
        print("Error: The input file is empty")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")

# Example usage
if __name__ == "__main__":
    input_file = "train-00003-of-00015.csv"
    create_language_pairs(input_file)