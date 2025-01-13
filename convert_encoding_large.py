import os
import chardet
import pandas as pd
import io

def detect_encoding(file_path):
    """
    Detect the encoding of a file with fallback strategies.
    
    Args:
        file_path (str): Path to the file
    
    Returns:
        str: Detected or fallback encoding
    """
    # List of encodings to try
    encodings_to_try = [
        'utf-8', 'latin-1', 'cp1252', 'iso-8859-1', 
        'utf-16', 'big5', 'shift_jis', 'gb18030'
    ]
    
    try:
        # First, try chardet on a sample of the file
        with open(file_path, 'rb') as file:
            # Read first 100KB to improve detection accuracy
            raw_data = file.read(100 * 1024)
        
        chardet_result = chardet.detect(raw_data)
        detected_encoding = chardet_result['encoding']
        
        # If chardet fails or returns None, use fallback encodings
        if not detected_encoding:
            for encoding in encodings_to_try:
                try:
                    raw_data.decode(encoding)
                    return encoding
                except UnicodeDecodeError:
                    continue
            
            # If all else fails, use latin-1 (can decode any byte)
            return 'latin-1'
        
        return detected_encoding
    except Exception as e:
        print(f"Error detecting encoding for {file_path}: {e}")
        return 'latin-1'  # Safest fallback

def convert_large_csv(file_path, chunk_size=100000):
    """
    Convert large CSV file to UTF-8-SIG encoding using chunked processing.
    
    Args:
        file_path (str): Path to the CSV file
        chunk_size (int): Number of rows to process in each chunk
    """
    try:
        # Detect original encoding
        original_encoding = detect_encoding(file_path)
        
        # Temporary output file
        temp_file_path = file_path + '.temp'
        
        # Read and write in chunks
        with open(file_path, 'r', encoding=original_encoding, errors='replace') as input_file, \
             open(temp_file_path, 'w', encoding='utf-8-sig', errors='replace') as output_file:
            
            # Read and write header
            header = input_file.readline()
            output_file.write(header)
            
            # Process file in chunks
            while True:
                chunk = input_file.readlines(chunk_size)
                if not chunk:
                    break
                
                # Write chunk to output file
                output_file.writelines(chunk)
        
        # Replace original file with converted file
        os.replace(temp_file_path, file_path)
        print(f"Converted {file_path} from {original_encoding} to UTF-8-SIG")
    
    except Exception as e:
        print(f"Error converting large CSV {file_path}: {e}")
        # Cleanup temporary file if it exists
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

def convert_large_excel(file_path, chunk_size=100000):
    """
    Convert large Excel file to UTF-8-SIG encoding using chunked processing.
    
    Args:
        file_path (str): Path to the Excel file
        chunk_size (int): Number of rows to process in each chunk
    """
    try:
        # Read Excel file in chunks
        excel_reader = pd.read_excel(file_path, engine='openpyxl', chunksize=chunk_size)
        
        # Temporary output file
        temp_file_path = file_path + '.temp'
        
        # Write chunks to new file
        first_chunk = True
        for chunk in excel_reader:
            if first_chunk:
                # Write first chunk with headers
                chunk.to_excel(temp_file_path, index=False, encoding='utf-8-sig')
                first_chunk = False
            else:
                # Append subsequent chunks
                chunk.to_excel(temp_file_path, index=False, encoding='utf-8-sig', mode='a', header=False)
        
        # Replace original file with converted file
        os.replace(temp_file_path, file_path)
        print(f"Converted {file_path} to UTF-8-SIG")
    
    except Exception as e:
        print(f"Error converting large Excel file {file_path}: {e}")
        # Cleanup temporary file if it exists
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

def convert_file_encoding(file_path):
    """
    Convert file to UTF-8-SIG encoding with robust error handling.
    
    Args:
        file_path (str): Path to the file
    """
    try:
        # Get file extension
        _, ext = os.path.splitext(file_path)
        ext = ext.lower()
        
        # Handle different file types
        if ext == '.csv':
            convert_large_csv(file_path)
        elif ext == '.xlsx':
            convert_large_excel(file_path)
        elif ext == '.txt':
            # For text files, use standard conversion
            original_encoding = detect_encoding(file_path)
            with open(file_path, 'r', encoding=original_encoding, errors='replace') as file:
                content = file.read()
            
            with open(file_path, 'w', encoding='utf-8-sig', errors='replace') as file:
                file.write(content)
            print(f"Converted {file_path} from {original_encoding} to UTF-8-SIG")
        else:
            print(f"Unsupported file type: {ext}")
    
    except Exception as e:
        print(f"Error converting {file_path}: {e}")

def convert_files_in_directory(directory='.'):
    """
    Convert all .txt, .csv, and .xlsx files in a directory to UTF-8-SIG.
    
    Args:
        directory (str): Directory path to process files in
    """
    # Supported file extensions
    supported_extensions = ['.txt', '.csv', '.xlsx']
    
    # Iterate through files in the directory
    for filename in os.listdir(directory):
        # Check if file has supported extension
        if any(filename.lower().endswith(ext) for ext in supported_extensions):
            file_path = os.path.join(directory, filename)
            convert_file_encoding(file_path)

def main():
    # Convert files in the current directory
    convert_files_in_directory()

if __name__ == "__main__":
    main()