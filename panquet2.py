# import pandas as pd
# import os

# def parquet_to_csv(input_file, output_file_prefix, rows_per_file=1000000):
#     try:
#         # Read the Parquet file
#         print(f"Reading Parquet file: {input_file}")
#         data = pd.read_parquet(input_file)
        
#         # Ensure the expected columns exist
#         expected_columns = ['french', 'fon']
#         if not all(col in data.columns for col in expected_columns):
#             raise ValueError(f"The Parquet file does not contain the required columns: {expected_columns}")

#         # Split into multiple files if necessary
#         total_rows = len(data)
#         num_files = (total_rows // rows_per_file) + (1 if total_rows % rows_per_file != 0 else 0)
        
#         print(f"Total rows: {total_rows}. Splitting into {num_files} file(s).")

#         for i in range(num_files):
#             start_row = i * rows_per_file
#             end_row = min(start_row + rows_per_file, total_rows)
#             output_file = f"{output_file_prefix}_part{i+1}.csv"

#             # Write the chunk to a CSV file
#             print(f"Writing rows {start_row} to {end_row} to {output_file}")
#             data.iloc[start_row:end_row].to_csv(output_file, index=False, encoding='utf-8-sig')

#         print("Conversion complete.")

#     except FileNotFoundError:
#         print(f"Error: The file {input_file} does not exist.")
#     except ValueError as ve:
#         print(f"ValueError: {ve}")
#     except Exception as e:
#         print(f"An unexpected error occurred: {e}")

# # Example usage
# input_parquet_file = "train.parquet"
# output_csv_prefix = "train"
# parquet_to_csv(input_parquet_file, output_csv_prefix)


import pandas as pd
import os

def parquet_to_csv(input_file, output_file_prefix, rows_per_file=1000000):
    try:
        # Read the Parquet file
        print(f"Reading Parquet file: {input_file}")
        data = pd.read_parquet(input_file)
        
        # Ensure the expected columns exist
        expected_columns = ['text', 'language']
        if not all(col in data.columns for col in expected_columns):
            raise ValueError(f"The Parquet file does not contain the required columns: {expected_columns}")

        # Split into multiple files if necessary
        total_rows = len(data)
        num_files = (total_rows // rows_per_file) + (1 if total_rows % rows_per_file != 0 else 0)
        
        print(f"Total rows: {total_rows}. Splitting into {num_files} file(s).")

        for i in range(num_files):
            start_row = i * rows_per_file
            end_row = min(start_row + rows_per_file, total_rows)
            output_file = f"{output_file_prefix}_part{i+1}.csv"

            # Write the chunk to a CSV file
            print(f"Writing rows {start_row} to {end_row} to {output_file}")
            data.iloc[start_row:end_row].to_csv(output_file, index=False, encoding='utf-8-sig')

        # Validation
        print("Validating data alignment...")
        reloaded_data = pd.concat(
            pd.read_csv(f"{output_file_prefix}_part{i+1}.csv", encoding='utf-8-sig')
            for i in range(num_files)
        )

        if data.equals(reloaded_data):
            print("Validation successful: Data alignment is preserved.")
        else:
            raise ValueError("Validation failed: Data mismatch detected between Parquet and CSV.")

        print("Conversion complete.")

    except FileNotFoundError:
        print(f"Error: The file {input_file} does not exist.")
    except ValueError as ve:
        print(f"ValueError: {ve}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Example usage
input_parquet_file = "train-00000-of-00001.parquet"
output_csv_prefix = "train-00000-of-00001"
parquet_to_csv(input_parquet_file, output_csv_prefix)

