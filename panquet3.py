import pandas as pd

def parquet_to_csv(input_parquet_path, output_csv_path):
    """
    Convert a Parquet file to CSV, extracting only Bambara and French translations

    Parameters:
    input_parquet_path (str): Path to input Parquet file (e.g., 'data.parquet')
    output_csv_path (str): Path for output CSV file (e.g., 'translations.csv')
    """
    # Read the Parquet file
    df = pd.read_parquet(input_parquet_path)

    # Select only bambara and french columns
    translations_df = df[['instruction', 'input', 'output']]

    # Export to CSV with UTF-8-SIG encoding
    translations_df.to_csv(output_csv_path, index=False, encoding='utf-8-sig')

    print(f"Successfully exported translations to {output_csv_path}")
    print(f"Number of rows exported: {len(translations_df)}")

# Example usage:
parquet_to_csv('train-00000-of-00001.parquet', 'train-00000-of-00001.csv')

