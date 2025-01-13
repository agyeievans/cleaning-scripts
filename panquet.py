import pandas as pd
import pyarrow.parquet as pq

def read_parquet_sample(file_path):
    """
    Read and display the first 10 rows of a Parquet file.
    
    Args:
        file_path (str): Path to the Parquet file
    """
    try:
        # Read the Parquet file
        df = pd.read_parquet(file_path)
        
        # Get all column names
        columns = df.columns
        print("\nColumns in the Parquet file:")
        print("----------------------------")
        for i, col in enumerate(columns, 1):
            print(f"{i}. {col}")
            
        # Display the first 10 rows with all columns
        print("\nFirst 10 rows of data:")
        print("----------------------")
        print(df.head(10).to_string())
        
        # Display basic information about the dataset
        print("\nDataset Info:")
        print("-------------")
        print(f"Total number of rows: {len(df)}")
        print(f"Total number of columns: {len(columns)}")
        
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except Exception as e:
        print(f"Error reading the Parquet file: {str(e)}")

# Example usage
if __name__ == "__main__":
    # Replace 'your_file.parquet' with your Parquet file path
    file_path = 'afr_Latn test.parquet'
    read_parquet_sample(file_path)