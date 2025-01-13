import os
import chardet
import pandas as pd

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
        # First, try chardet
        with open(file_path, 'rb') as file:
            raw_data = file.read()
        
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

def convert_file_encoding(file_path):
    """
    Convert file to UTF-8-SIG encoding with robust error handling.
    
    Args:
        file_path (str): Path to the file
    """
    try:
        # Detect original encoding
        original_encoding = detect_encoding(file_path)
        
        # Get file extension
        _, ext = os.path.splitext(file_path)
        ext = ext.lower()
        
        # Handle different file types
        if ext in ['.txt', '.csv']:
            # Read text/CSV files with error handling
            with open(file_path, 'r', encoding=original_encoding, errors='replace') as file:
                content = file.read()
            
            # Write with UTF-8-SIG encoding
            with open(file_path, 'w', encoding='utf-8-sig', errors='replace') as file:
                file.write(content)
            print(f"Converted {file_path} from {original_encoding} to UTF-8-SIG")
        
        elif ext == '.xlsx':
            # Read Excel file
            try:
                df = pd.read_excel(file_path, engine='openpyxl')
            except Exception as e:
                print(f"Error reading Excel file {file_path}: {e}")
                return
            
            # Write Excel file with UTF-8-SIG encoding
            df.to_excel(file_path, index=False, encoding='utf-8-sig')
            print(f"Converted {file_path} to UTF-8-SIG")
        
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