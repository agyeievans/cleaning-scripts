import pyarrow.parquet as pq
import pandas as pd

def process_large_parquet_to_split_csv(parquet_file, output_csv_base, rows_per_file=1000000):
    # Open the Parquet file for reading
    parquet_file_reader = pq.ParquetFile(parquet_file)
    file_index = 0
    total_rows_written = 0

    # Process the file in row group chunks
    for row_group in range(parquet_file_reader.num_row_groups):
        # Read a row group as a DataFrame
        table = parquet_file_reader.read_row_group(row_group)
        df_chunk = table.to_pandas()

        # Ensure the 'translation' column contains dictionaries
        if not df_chunk['translation'].apply(lambda x: isinstance(x, dict)).all():
            raise ValueError("The 'translation' column must contain dictionaries.")

        # Extract 'arabic' and 'english' columns from the 'translation' column
        df_extracted = df_chunk['translation'].apply(pd.Series)
        
        # Check for Arabic and English columns
        if 'bam' not in df_extracted or 'fr' not in df_extracted:
            raise ValueError("The 'translation' column does not contain 'arabic' and 'english' keys.")

        # Write the DataFrame to CSV files, splitting as needed
        for start in range(0, len(df_extracted), rows_per_file - total_rows_written):
            end = start + rows_per_file - total_rows_written
            chunk_to_write = df_extracted.iloc[start:end]

            # Output file name with an incrementing index
            output_file = f"{output_csv_base}_{file_index + 1}.csv"
            
            # Write the chunk to a CSV file
            chunk_to_write.to_csv(
                output_file,
                mode='a',  # Append mode
                encoding='utf-8-sig',
                index=False,
                header=file_index == 0 and start == 0
            )
            total_rows_written += len(chunk_to_write)
            
            # If we hit the row limit for a file, move to the next one
            if total_rows_written >= rows_per_file:
                file_index += 1
                total_rows_written = 0

# Specify the input Parquet file and base name for output CSV files
parquet_file = "bam-fr_train_0000.parquet"
output_csv_base = "bam-fr_train_0000"

print("Processing large Parquet file to split CSV files...")

process_large_parquet_to_split_csv(parquet_file, output_csv_base)

print("CSV files created successfully!")